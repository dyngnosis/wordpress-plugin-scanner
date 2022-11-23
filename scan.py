import urllib.request, re, time, sys
wordpress_server = 'http://plugins.svn.wordpress.org'
target_server = 'http://www.scopesecurity.com'

def getPluginList():
    pluginpage = urllib.request.urlopen\
        ("http://plugins.svn.wordpress.org/",).read().decode('utf-8')
    regex = re.compile(r'<li><a href="(.*?)/')
    return regex.findall(pluginpage)

def getPluginVersion(plugin):
    regex = re.compile(r'Stable tag: ([0-9]?\.?[0-9]?\.?[0-9]?\.?[0-9]?\.?[0-9])')
    plugin_base_url = "http://plugins.svn.wordpress.org/"
    plugin_readme_path = '/trunk/readme.txt'
    plugin_url = plugin_base_url + plugin + plugin_readme_path
    readme = urllib.request.urlopen(plugin_url).read().decode('utf-8')
    version = regex.findall(readme)
    return version[0]

def findPlugins(plugins):
    plugin_versions={}
    print("Scanning for " + str(plugins.__len__()) +" plugins")
    for plugin in plugins:
        regex = re.compile(r'Stable tag: ([0-9]?\.?[0-9]?\.?[0-9]?\.?[0-9]?\.?[0-9])')
        try:
            readme = urllib.request.urlopen(target_server + "/wp-content/plugins/" +plugin+"/readme.txt",).read().decode('utf-8')
            version = regex.findall(readme)
            if version != []:
                print(time.localtime())
                print("Plugin found: \"" + plugin + "\" Installed Version:" + version[0]+" Current Version:"+getPluginVersion(plugin)+"\n")
        except urllib.error.HTTPError as e:
            if e.code == 403:
                pass
            else:
                print(e)
            
            
            

    return plugin_versions

plugins =  getPluginList()
installed_plugins = findPlugins(plugins)
