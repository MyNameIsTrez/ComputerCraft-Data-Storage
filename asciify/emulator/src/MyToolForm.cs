using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Net.WebSockets;
using System.Windows.Forms;

using BizHawk.Client.Common;
using BizHawk.WinForms.Controls;

namespace Net.MyStuff.MyTool
{
	[ExternalTool("MyTool")]
	public sealed class MyToolForm : Form, IExternalToolForm
	{
		[RequiredApi]
		public ICommApi? _maybeCommAPI { get; set; }

		[RequiredApi]
		public IEmuClientApi? _maybeClientAPI { get; set; }

		[RequiredApi]
		public IEmulationApi? _maybeEmuAPI { get; set; }

		[RequiredApi]
		public IGameInfoApi? _maybeGameInfoAPI { get; set; }

		[RequiredApi]
		public IGuiApi? _maybeGuiAPI { get; set; }

		[RequiredApi]
		public IMemoryApi? _maybeMemAPI { get; set; }

		[RequiredApi]
		public IJoypadApi? _maybeJoypadAPI { get; set; }

		private ApiContainer? _apis;

		private ApiContainer APIs => _apis ??= new ApiContainer(new Dictionary<Type, IExternalApi>
		{
			[typeof(ICommApi)] = _maybeCommAPI ?? throw new NullReferenceException(),
			[typeof(IEmuClientApi)] = _maybeClientAPI ?? throw new NullReferenceException(),
			[typeof(IEmulationApi)] = _maybeEmuAPI ?? throw new NullReferenceException(),
			[typeof(IGameInfoApi)] = _maybeGameInfoAPI ?? throw new NullReferenceException(),
			[typeof(IGuiApi)] = _maybeGuiAPI ?? throw new NullReferenceException(),
			[typeof(IMemoryApi)] = _maybeMemAPI ?? throw new NullReferenceException(),
			[typeof(IJoypadApi)] = _maybeJoypadAPI ?? throw new NullReferenceException()
		});

		public MyToolForm()
		{
			ClientSize = new Size(200, 200);
			Text = "BizHawkCC";

			Load += (sender, args) => {
				OpenRom();
				Connect();
				Console.WriteLine("\nRunning game:");
				//Console.WriteLine(string.Join("\n", APIs.Joypad.Get().Select((k, v) => $"{k}: {v}")));
			};
		}

		public void OpenRom() {
			Console.WriteLine("\nOpening ROM...");
			APIs.EmuClient.OpenRom("../Super_Mario_Bros.nes");
		}

		public void Connect() {
			Console.WriteLine("\nCreating connection with Node.js...");
		}

		public bool AskSaveChanges() => true;

		public void Restart() {}

		private int frameCount = 0;

		public void UpdateValues(ToolFormUpdateType type)
		{
			if (type != ToolFormUpdateType.PreFrame && type != ToolFormUpdateType.FastPreFrame) return;

			if (frameCount % 100 == 99) TakeScreenshot();
	    		frameCount++;

			PressKey();
		}

		public void TakeScreenshot() {
			APIs.EmuClient.Screenshot();
			Console.WriteLine("Screenshot taken");
		}

		public void PressKey() {
			APIs.Joypad.Set("Right", true, 1);
		}
	}
}
