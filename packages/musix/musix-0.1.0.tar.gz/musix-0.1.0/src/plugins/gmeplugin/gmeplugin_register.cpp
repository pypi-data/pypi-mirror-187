#include "GMEPlugin.h"
namespace musix {
static ChipPlugin::RegisterMe registerMe([](const std::string &configDir) -> std::shared_ptr<GMEPlugin> { return std::make_shared<GMEPlugin>(); });
}
