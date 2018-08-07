# SlideFramework v1
SlideFramework is a presentation engine written in Python that allows you to make a fully interactive presentation written in HTML5 with the possibility of extend kernel with modules.

## Simple usage.
`./slideframework.py --slides pathwithyourslide`

### Other options
 - --port: Where do you want to listen?
 - --template: What template do you want to use?
 
 ## Create your first slide.
 - Create an empty folder at your computer, and copy the content of slide_test inside.
 - Edit configuration.json with your settings.
 
 ## Advanced features
 ### LaTeX Support
 Just write LaTeX content between $$ $$, example:
 ``` $$ x^2+b x + c $$ ```
 ### Slide paths
 You can load content from your slides folder just by: http://localhost/my-presentation/file where file is a file inside slide path.
 ### Modules
 You can load content from your modules folder just by: http://localhost/my-modules/key where key is the key at configuration.json
 
 ### Trigger when SlideFramework is loaded:
 ```$('body').on('slideframework__configuration__loaded', callback);```
 
 ### Trigger when the slide change
 ```$('body').on('slideframework__next__slide', callback);```
 
 ```$('body').on('slideframework__previous__slide', callback);```
 
 ```$('body').on('slideframework__slide__loaded', callback);```

 
