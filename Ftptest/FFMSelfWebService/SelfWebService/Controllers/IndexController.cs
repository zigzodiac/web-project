using SelfWebService.Models;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Web.Http;
using System.Web.Http.Description;

namespace SelfWebService.Controllers
{
    public class IndexController : ApiController
    {
        public HttpResponseMessage Get()
        {
            string viewPath = System.IO.Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Views\\index.html");

            string indexPage;

            using (StreamReader stream = new StreamReader(viewPath))
            {
                indexPage = stream.ReadToEnd();
            }

            return new HttpResponseMessage
            {
                Content = new StringContent(indexPage, Encoding.UTF8, "text/html")
            };
        }
    }
}
