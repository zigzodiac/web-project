using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SelfWebService.Models
{
    public class File
    {
        public string Local { get; set; }
        public string Ftp { get; set; }
    }

    public class FileModel
    {
        public string Name { get; set; }
        public List<File> Files { get; set; }
    }
}
