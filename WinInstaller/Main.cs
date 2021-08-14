using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.IO.Compression;
using System.Threading;

namespace WinInstaller
{
    public partial class Main : Form
    {
        public Main()
        {
            InitializeComponent();
        }

        private void status(string statusStr)
        {
            StatusBox.AppendText(statusStr + "\n");
        }

        private string blenderDir = $"{Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData)}\\Blender Foundation\\Blender";
        private string latestDownload = "https://github.com/robiot/blendpresence/archive/refs/heads/main.zip";
        private string downloadFolder = $"tmpDownload";

        private void Main_Load(object sender, EventArgs e)
        {
            try
            {
                foreach (string version in Directory.GetDirectories(blenderDir))
                {
                    BlenderVersions.Items.Add(new DirectoryInfo(version).Name);
                }
                BlenderVersions.SelectedIndex = 0;
            }
            catch (Exception)
            {
                status("Error when finding blender versions. Is blender installed?");
                InstallButton.Enabled = false;
            }
        }


        private void InstallButton_Click(object sender, EventArgs e)
        {
            InstallButton.Enabled = false;
            StatusBox.Clear();
            // Create Download Dir If Not exist
            status("Checking if tmpDir exists.");
            if (Directory.Exists(downloadFolder))
            {
                status("Exists, Removing all contents.");
                DeleteContents(downloadFolder);
            }
            else
            {
                status("Didn't exist. Creating!");
                Directory.CreateDirectory(downloadFolder);
            }


            Thread thread = new Thread(() => {
                WebClient client = new WebClient();
                client.DownloadProgressChanged += new DownloadProgressChangedEventHandler(client_DownloadProgressChanged);
                client.DownloadFileCompleted += new AsyncCompletedEventHandler(client_DownloadFileCompleted);
                try
                {
                    client.DownloadFileAsync(new Uri(latestDownload), $"{downloadFolder}\\main.zip");
                }
                catch
                {
                    status("An Error occured while downloading. Are you connected to the internet?");
                    InstallButton.Enabled = true;
                    return;
                }
            });
            thread.Start();
        }

        private void MoveFiles()
        {
            try
            {
                status("Extracting Archive.");
                ZipFile.ExtractToDirectory($"{downloadFolder}\\main.zip", $"{downloadFolder}\\main");
            }
            catch (Exception ex)
            {
                status("Could not extract the ZipFile: " + ex.Message);
                InstallButton.Enabled = true;
                return;
            }

            string blendDir = $"{blenderDir}\\{BlenderVersions.Text}\\scripts\\addons";
            string blendpresenceDir = $"{blendDir}\\blendpresence";
            status("Checking if Blender exists in Appdata.");
            if (!Directory.Exists(blendDir))
            {
                status("Didn't exist. Creating");
                Directory.CreateDirectory(blendDir);
            }

            status("Checking if blendpresence already is installed.");
            if (Directory.Exists(blendpresenceDir))
            {
                status("Installed, Removing all contents for update.");
                DirectoryInfo folder = new DirectoryInfo(blendpresenceDir);

                foreach (FileInfo file in folder.GetFiles())
                {
                    status($"Removing {file.Name}");
                    file.Delete();
                }
                foreach (DirectoryInfo dir in folder.GetDirectories())
                {
                    status($"Removing {dir.Name}");
                    dir.Delete(true);
                }
            }
            else
            {
                status("Didn't exist. Creating!");
                Directory.CreateDirectory(blendpresenceDir);
            }


            if (CopyFiles($"{downloadFolder}\\main\\blendpresence-main", blendpresenceDir) == -1)
            {
                status("Installation Failed");
                InstallButton.Enabled = true;
                return;
            }

            status("Cleaning up.");
            DeleteContents(downloadFolder);
            Directory.Delete(downloadFolder);

            status("Sucessfully Installed Blenderpresence.");
            status("\nNow you can activate it from the add-ons tab in blenders Preferences");
            InstallButton.Enabled = true;
        }

        void client_DownloadProgressChanged(object sender, DownloadProgressChangedEventArgs e)
        {
            this.BeginInvoke((MethodInvoker)delegate {
                status($"Downloaded {e.BytesReceived} of {e.TotalBytesToReceive}.");
            });
        }
        void client_DownloadFileCompleted(object sender, AsyncCompletedEventArgs e)
        {
            this.BeginInvoke((MethodInvoker)delegate {
                status("Completed Download.");
                MoveFiles();
            });
        }

        private void DeleteContents(string folderStr)
        {
            DirectoryInfo folder = new DirectoryInfo(folderStr);

            foreach (FileInfo file in folder.GetFiles())
            {
                status($"Removing {file.Name}");
                file.Delete();
            }
            foreach (DirectoryInfo dir in folder.GetDirectories())
            {
                status($"Removing {dir.Name}");
                dir.Delete(true);
            }
        }

        int CopyFiles(string sourcePath, string targetPath)
        {
            try
            {
                foreach (string dirPath in Directory.GetDirectories(sourcePath, "*", SearchOption.AllDirectories))
                {
                    Directory.CreateDirectory(dirPath.Replace(sourcePath, targetPath));
                }

                foreach (string newPath in Directory.GetFiles(sourcePath, "*.*", SearchOption.AllDirectories))
                {
                    status("Copying files");
                    File.Copy(newPath, newPath.Replace(sourcePath, targetPath), true);
                }
            }
            catch (Exception ex)
            {
                status(ex.Message);
                return -1;
            }
            return 1;
        }
    }
}
