using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http.Formatting;
using System.Text;
using System.Web.Http;
using System.Web.Http.SelfHost;
using SelfWebService.Controllers;

namespace SelfWebService
{
    class Program
    {
        static void Main(string[] args)
        {
            AppMain app = new AppMain();
            app.StartSelfWebHost();
        }
    }
}
