#include "script.hpp"
#include "colors.hpp"

#include <ansi/console.h>
#include <coreutils/utils.h>

#include <fmt/format.h>
#include <sol/sol.hpp>

Script::Script()
{
    lua_state = std::make_unique<sol::state>();
    auto& lua = *lua_state;

    lua.open_libraries(sol::lib::base, sol::lib::string, sol::lib::table,
                       sol::lib::io);
}

bool Script::handle_key(int key)
{
    auto it = mapping.find(key);
    if (it != mapping.end()) {
        it->second();
        return true;
    }
    return false;
}

void Script::start()
{
    auto& lua = *lua_state;

    for (auto&& [name, color] : html_colors) {
        lua[utils::toUpper(name)] = (color << 8) | 0xff;
    }
    lua["DEFAULT"] = 0x12345600;

    for (int i = KEY_F1; i <= KEY_F8; i++) {
        lua[fmt::format("KEY_F{}", i - KEY_F1 + 1)] = i;
    }

    lua["get_meta"] = [&] {
        sol::table t = lua.create_table();
        for (auto [name, val] : meta) {
            std::visit([&, n = name](auto&& v) { t[n] = v; }, val);
        }
        return t;
    };
    lua.set_function("var_color",
                     sol::overload(
                         [&](std::string const& var, uint32_t color) {
                             if (auto* target = panel.get_var(var)) {
                                 target->fg = color;
                             }
                         },
                         [&](std::string const& var, uint32_t fg, uint32_t bg) {
                             if (auto* target = panel.get_var(var)) {
                                 target->fg = fg;
                                 target->bg = bg;
                             }
                         }));
    lua.set_function("map",
                     sol::overload(
                         [&](std::string key, std::function<void()> const& fn) {
                             mapping[static_cast<int>(key[0])] = fn;
                         },
                         [&](int key, std::function<void()> const& fn) {
                             mapping[key] = fn;
                         }));

    lua.set_function(
        "colorize",
        sol::overload(
            [&](std::string const& pattern, uint32_t color) {
                auto [x, y] = con->find(pattern);
                if (x >= 0) {
                    con->set_color(color);
                    con->colorize(x, y, pattern.size(), 1);
                }
            },
            [&](std::string const& pattern, uint32_t fg, uint32_t bg) {
                auto [x, y] = con->find(pattern);
                if (x >= 0) {
                    con->set_color(fg, bg);
                    con->colorize(x, y, pattern.size(), 1);
                }
            },
            [&](int x, int y, int len, uint32_t color) {
                con->set_color(color);
                con->colorize(x, y, len, 1);
            },
            [&](int x, int y, int len, uint32_t fg, uint32_t bg) {
                con->set_color(fg, bg);
                con->colorize(x, y, len, 1);
            }));

    lua["set_theme"] = [&](sol::table args) {
        theme_set = true;
        std::string panelText = args["panel"];
        auto panel_bg =
            args.get_or<uint32_t>("panel_bg", bbs::Console::DefaultColor);
        auto panel_fg =
            args.get_or<uint32_t>("panel_fg", bbs::Console::DefaultColor);
        auto var_bg =
            args.get_or<uint32_t>("var_bg", bbs::Console::DefaultColor);
        auto var_fg =
            args.get_or<uint32_t>("var_fg", bbs::Console::DefaultColor);
        con->set_color(panel_fg, panel_bg);
        panel.set_color(var_fg, var_bg);
        panel.set_panel(panelText);
        sol::function v = args["init_fn"];
        if (v.valid()) { v(); }
        con->set_color(panel_fg, panel_bg);
        update_fn = args["update_fn"];
    };

    auto dataPath = MusicPlayer::findDataPath("init.lua");

    if (!dataPath.empty() && fs::exists(dataPath)) {
        auto res = lua.script_file(dataPath.string());
        if (!res.valid()) { fmt::print("ERROR\n"); }
    }
}

void Script::update()
{
    if (update_fn.valid()) {
        sol::table t = lua.create_table();
        for (auto [name, val] : meta) {
            std::visit([&, n = name](auto&& v) { t[n] = v; }, val);
        }
        update_fn(t);
        for (auto&& [key, val] : t) {
            if (val.get_type() == sol::type::number) {
                meta[key.as<std::string>()] = val.as<uint32_t>();
            } else {
                meta[key.as<std::string>()] = val.as<std::string>();
            }
        }
    }
}
