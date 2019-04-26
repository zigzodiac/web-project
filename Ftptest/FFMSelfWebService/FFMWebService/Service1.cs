using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.ServiceProcess;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Timers;
using SelfWebService;

// C:\Windows\Microsoft.NET\Framework\v4.0.30319\InstallUtil.exe D:\FFM\T\FFM-Pipeline\code\FFMSelfWebService\FFMWebService\bin\Release\FFMWebService.exe
// net start FFMRenderWebService

// net stop FFMRenderWebService
// C:\Windows\Microsoft.NET\Framework\v4.0.30319\InstallUtil.exe -u D:\FFM\T\FFM-Pipeline\code\FFMSelfWebService\FFMWebService\bin\Release\FFMWebService.exe

namespace FFMWebService
{
    public partial class Service1 : ServiceBase
    {
        SelfWebService.AppMain webApp = new SelfWebService.AppMain();

        public Service1()
        {
            InitializeComponent();
        }

        protected override void OnStart(string[] args)
        {
            webApp.StartSelfWebHost();
        }

        protected override void OnStop()
        {
        }
    }
}
