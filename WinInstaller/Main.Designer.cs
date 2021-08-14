
namespace WinInstaller
{
    partial class Main
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Main));
            this.BlenderVersions = new System.Windows.Forms.ComboBox();
            this.InstallButton = new System.Windows.Forms.Button();
            this.StatusBox = new System.Windows.Forms.RichTextBox();
            this.versionLbl = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // BlenderVersions
            // 
            this.BlenderVersions.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.BlenderVersions.FormattingEnabled = true;
            this.BlenderVersions.Location = new System.Drawing.Point(218, 242);
            this.BlenderVersions.Name = "BlenderVersions";
            this.BlenderVersions.Size = new System.Drawing.Size(121, 21);
            this.BlenderVersions.TabIndex = 0;
            // 
            // InstallButton
            // 
            this.InstallButton.Location = new System.Drawing.Point(12, 272);
            this.InstallButton.Name = "InstallButton";
            this.InstallButton.Size = new System.Drawing.Size(327, 48);
            this.InstallButton.TabIndex = 1;
            this.InstallButton.Text = "Install Latest";
            this.InstallButton.UseVisualStyleBackColor = true;
            this.InstallButton.Click += new System.EventHandler(this.InstallButton_Click);
            // 
            // StatusBox
            // 
            this.StatusBox.Location = new System.Drawing.Point(12, 12);
            this.StatusBox.Name = "StatusBox";
            this.StatusBox.ReadOnly = true;
            this.StatusBox.Size = new System.Drawing.Size(327, 206);
            this.StatusBox.TabIndex = 2;
            this.StatusBox.Text = "";
            // 
            // versionLbl
            // 
            this.versionLbl.AutoSize = true;
            this.versionLbl.Font = new System.Drawing.Font("Segoe UI", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.versionLbl.Location = new System.Drawing.Point(12, 242);
            this.versionLbl.Name = "versionLbl";
            this.versionLbl.Size = new System.Drawing.Size(107, 19);
            this.versionLbl.TabIndex = 4;
            this.versionLbl.Text = "Blender Version:";
            // 
            // Main
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(351, 332);
            this.Controls.Add(this.versionLbl);
            this.Controls.Add(this.StatusBox);
            this.Controls.Add(this.InstallButton);
            this.Controls.Add(this.BlenderVersions);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "Main";
            this.Text = "BlendPresence Online Installer";
            this.Load += new System.EventHandler(this.Main_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ComboBox BlenderVersions;
        private System.Windows.Forms.Button InstallButton;
        private System.Windows.Forms.RichTextBox StatusBox;
        private System.Windows.Forms.Label versionLbl;
    }
}

