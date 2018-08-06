# Copyright (c) 2018 José Carlos García (hola@josecarlos.me)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import os, json, re
import importlib.util


class SlideFramework:
    templatedir  = ''
    slidesdir    = ''
    slidesconfig = {}
    @staticmethod
    def startengine(template, slides):
        print('Starting SlideFramework with template', template)
        SlideFramework.templatedir = os.path.realpath('templates/{}.html'.format(template))
        SlideFramework.slidesdir   = os.path.realpath(slides)
        
        if not os.path.exists(SlideFramework.templatedir):
            raise Exception('Template not found! ({})'.format(SlideFramework.templatedir))

        if not os.path.exists(SlideFramework.slidesdir):
            raise Exception('Slides path not found! ({})'.format(SlideFramework.slidesdir))

        configurationpath = os.path.join(SlideFramework.slidesdir, "configuration.json")

        if not os.path.exists(configurationpath):
            raise Exception('Configuration file expected! {}'.format(configurationpath))

        configuration = open(configurationpath, 'r')
        
        configurationRaw = configuration.read()
        configurationRaw = re.sub(r"(^)?[^\S\n]*/(?:.*(.*?)*/[^\S\n]*|/[^\n]*)($)?", '', configurationRaw)

        SlideFramework.slidesconfig = json.loads(configurationRaw)
        configuration.close()

        SlideFramework.modules = {}

        # Load external modules.
        if "modules" in SlideFramework.slidesconfig.keys():
            modules = SlideFramework.slidesconfig['modules']

            for handler, module in modules.items():
                modulepath = os.path.join(SlideFramework.slidesdir, module)
                spec = importlib.util.spec_from_file_location(handler, modulepath)
                modulefunc = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modulefunc)

                SlideFramework.modules[handler] = modulefunc.run_module


    @staticmethod
    def indexresponse():
        index = ''

        templatefile = open(SlideFramework.templatedir, 'r')

        index       += templatefile.read()

        replacements = {'title' : SlideFramework.slidesconfig['title']}

        for key, value in replacements.items():
            index    = index.replace('%{}%'.format(key), value)
            
        templatefile.close()
        return str.encode(index)
