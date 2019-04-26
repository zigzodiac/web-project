using SelfWebService.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Web.Http;

namespace SelfWebService.Controllers
{
    public class FilesController : ApiController
    {
        [ActionName("Log")]
        public string[] GetLog()
        {
            string logFile = System.IO.Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "log.txt");

            if (System.IO.File.Exists(logFile))
            {
                string[] logMessages = System.IO.File.ReadAllLines(logFile, Encoding.UTF8);
                return logMessages;
            }
            return null;
        }

        [ActionName("Copy")]
        public HttpResponseMessage Post(FileModel item)
        {
            // Copy Files Ftp to Local
            foreach (File _file in item.Files)
            {
                try
                {
                    string now = DateTime.Now.ToString("yyyy/MM/dd hh:mm:ss tt");
                    string message = string.Format("[{0} - {1}] : '{2}' Copy to '{3}'", now, item.Name, _file.Ftp, _file.Local);
                    Console.WriteLine(message);
                    System.IO.File.Copy(_file.Ftp, _file.Local, true);

                    string logFile = System.IO.Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "log.txt");
                    System.IO.File.AppendAllText(logFile, message + Environment.NewLine);
                }
                catch (System.IO.IOException e)
                {
                    Console.WriteLine("Error : '{0}'", e.Message);
                }
            }
            Console.WriteLine("Copy Finish : {0}", item.Name);

            var response = Request.CreateResponse<FileModel>(HttpStatusCode.Created, item);
            string uri = Url.Link("ActionApi", new {});
            response.Headers.Location = new Uri(uri);

            return response;
        }
    }
}
