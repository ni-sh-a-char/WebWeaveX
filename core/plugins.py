PLUGINS = {
    "pre_extract": [],
    "post_extract": [],
    "pre_crawl": [],
    "post_crawl": []
}


def register_plugin(stage, func):
    if stage in PLUGINS:
        PLUGINS[stage].append(func)


def run_plugins(stage, data):
    if stage not in PLUGINS:
        return data
    
    for plugin in PLUGINS[stage]:
        try:
            data = plugin(data)
        except Exception:
            pass
    
    return data