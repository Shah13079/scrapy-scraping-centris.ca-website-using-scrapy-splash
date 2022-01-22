User_Agnets = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"

Splash_lua_script ="""
function main(splash, args)
  
    splash.images_enabled=false
    splash.js_enabled=false
  	splash.css_enabled=false
  	splash.plugins_enabled=false
  
  	--Aborting request to css file
  	splash:on_request(function(request)
      if string.find(request.url,".css") then
          request.abort()
      end
    end)
   
    assert(splash:go(args.url))
    assert(splash:wait(0.5))
  

    return {
        html = splash:html(),
     		har = splash:har(),
    		
    }
end

 """

 

                                   
