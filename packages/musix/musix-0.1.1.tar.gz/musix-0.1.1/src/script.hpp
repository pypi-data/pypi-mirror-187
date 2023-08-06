#pragma once
#include <sol/forward.hpp>
#include <memory>
#include <unordered_map>
#include <functional>

class Script
{
    std::unordered_map<int, std::function<void()>> mapping;
    std::unique_ptr<sol::state> lua_state;

    bool theme_set = false;
    //sol::function update_fn;

    Script();
    void start();

    bool handle_key(int key);
    void update();
};
