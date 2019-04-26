using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web.Http;
using System.Web.Http.SelfHost;

namespace SelfWebService
{
    public class AppMain
    {
        public void StartSelfWebHost()
        {
            var config = new HttpSelfHostConfiguration("http://localhost:8080");

            config.Routes.MapHttpRoute(
                name: "Index",
                routeTemplate: "{controller}.html",
                defaults: new { controller = "index" });

            config.Routes.MapHttpRoute(
                name: "DefaultApi",
                routeTemplate: "api/{controller}"
            );

            config.Routes.MapHttpRoute(
                name: "ActionApi",
                routeTemplate: "api/{controller}/{action}"
            );

            using (HttpSelfHostServer server = new HttpSelfHostServer(config))
            {
                server.OpenAsync().Wait();
                while(true)
                {
                }
                //Console.WriteLine("Press Enter to quit.");
                //Console.ReadLine();
            }
        }
    }
}
