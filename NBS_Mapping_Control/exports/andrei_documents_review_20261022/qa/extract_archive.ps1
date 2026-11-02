param([string]$InputArchive,[string]$Destination,[string]$Format='09',[switch]$ListOnly)
$ErrorActionPreference='Stop'
Add-Type -TypeDefinition @'
using System;
using System.IO;
using System.Collections.Generic;
using System.Runtime.InteropServices;
public static class ArchiveRead {
 [DllImport("kernel32",CharSet=CharSet.Unicode,SetLastError=true)] static extern IntPtr LoadLibrary(string path);
 [DllImport("kernel32",CharSet=CharSet.Ansi)] static extern IntPtr GetProcAddress(IntPtr lib,string name);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int Create(ref Guid cls,ref Guid iid,[MarshalAs(UnmanagedType.Interface)] out IInArchive archive);
 [StructLayout(LayoutKind.Explicit,Size=24)] public struct PV {
  [FieldOffset(0)] public ushort vt;
  [FieldOffset(8)] public IntPtr ptr;
  [FieldOffset(8)] public ulong number;
  public string Text {get{return vt==8?Marshal.PtrToStringBSTR(ptr):number.ToString();}}
 }
 [DllImport("ole32.dll")] static extern int PropVariantClear(ref PV p);
 [ComVisible(true),Guid("23170F69-40C1-278A-0000-000300030000"),InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
 public interface IInStream {
  [PreserveSig] int Read(IntPtr data,uint size,IntPtr processed);
  [PreserveSig] int Seek(long offset,uint origin,IntPtr newPosition);
 }
 [ComVisible(true),ClassInterface(ClassInterfaceType.None)] public class Input:IInStream {
  public FileStream F; public Input(string path){F=File.OpenRead(path);}
  public int Read(IntPtr data,uint size,IntPtr processed){try{byte[] b=new byte[(int)size];int n=F.Read(b,0,b.Length);Marshal.Copy(b,0,data,n);if(processed!=IntPtr.Zero)Marshal.WriteInt32(processed,n);return 0;}catch{return -2147467259;}}
  public int Seek(long offset,uint origin,IntPtr np){try{long n=F.Seek(offset,(SeekOrigin)origin);if(np!=IntPtr.Zero)Marshal.WriteInt64(np,n);return 0;}catch{return -2147467259;}}
 }
 [ComVisible(true),Guid("23170F69-40C1-278A-0000-000300020000"),InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
 public interface IOutStream { [PreserveSig] int Write(IntPtr data,uint size,IntPtr processed); }
 [ComVisible(true),ClassInterface(ClassInterfaceType.None)] public class Output:IOutStream {
  public FileStream F; public Output(string path){F=File.Create(path);}
  public int Write(IntPtr data,uint size,IntPtr processed){try{byte[] b=new byte[(int)size];Marshal.Copy(data,b,0,b.Length);F.Write(b,0,b.Length);if(processed!=IntPtr.Zero)Marshal.WriteInt32(processed,(int)size);return 0;}catch{return -2147467259;}}
 }
 [ComVisible(true),Guid("23170F69-40C1-278A-0000-000600200000"),InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
 public interface IExtract {
  [PreserveSig] int SetTotal(ulong total);
  [PreserveSig] int SetCompleted(IntPtr completed);
  [PreserveSig] int GetStream(uint index,[MarshalAs(UnmanagedType.Interface)] out IOutStream stream,int askMode);
  [PreserveSig] int PrepareOperation(int askMode);
  [PreserveSig] int SetOperationResult(int result);
 }
 [ComVisible(true),ClassInterface(ClassInterfaceType.None)] public class Callback:IExtract {
  public Dictionary<uint,string> Paths;public Output Current;
  public Callback(Dictionary<uint,string> paths){Paths=paths;}
  public int SetTotal(ulong v){return 0;} public int SetCompleted(IntPtr v){return 0;}
  public int GetStream(uint i,out IOutStream s,int mode){s=null;if(Current!=null){Current.F.Dispose();Current=null;}if(mode!=0||!Paths.ContainsKey(i))return 0;Directory.CreateDirectory(Path.GetDirectoryName(Paths[i]));Current=new Output(Paths[i]);s=Current;return 0;}
  public int PrepareOperation(int m){return 0;}
  public int SetOperationResult(int r){if(Current!=null){Current.F.Dispose();Current=null;}if(r!=0)throw new Exception("Archive extraction result "+r);return 0;}
 }
 [ComImport,Guid("23170F69-40C1-278A-0000-000600600000"),InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
 public interface IInArchive {
  [PreserveSig] int Open([MarshalAs(UnmanagedType.Interface)] IInStream stream,ref ulong max,IntPtr callback);
  [PreserveSig] int Close();
  [PreserveSig] int GetNumberOfItems(out uint count);
  [PreserveSig] int GetProperty(uint index,uint property,ref PV value);
  [PreserveSig] int Extract([In,MarshalAs(UnmanagedType.LPArray,SizeParamIndex=1)]uint[] indices,uint count,int testMode,[MarshalAs(UnmanagedType.Interface)] IExtract callback);
 }
 public static string[] Run(string dll,string input,string dest,string format,bool list){
  var lib=LoadLibrary(dll);if(lib==IntPtr.Zero)throw new Exception("DLL load "+Marshal.GetLastWin32Error());
  var create=(Create)Marshal.GetDelegateForFunctionPointer(GetProcAddress(lib,"CreateObject"),typeof(Create));
  Guid cls=new Guid("23170F69-40C1-278A-1000-000110"+format+"0000"),iid=typeof(IInArchive).GUID;
  IInArchive arc;Marshal.ThrowExceptionForHR(create(ref cls,ref iid,out arc));var ins=new Input(input);ulong max=1UL<<24;
  int hr=arc.Open(ins,ref max,IntPtr.Zero);if(hr!=0)throw new Exception("Open failed "+hr);
  uint count;Marshal.ThrowExceptionForHR(arc.GetNumberOfItems(out count));var lines=new List<string>();var paths=new Dictionary<uint,string>();
  string root=Path.GetFullPath(dest)+Path.DirectorySeparatorChar;
  for(uint i=0;i<count;i++){
   PV prop=new PV();Marshal.ThrowExceptionForHR(arc.GetProperty(i,3,ref prop));string name=prop.Text;PropVariantClear(ref prop);
   prop=new PV();arc.GetProperty(i,6,ref prop);bool dir=prop.number!=0;PropVariantClear(ref prop);
   lines.Add(i+" "+name);
   if(!dir){string final=Path.GetFullPath(Path.Combine(root,name.Replace('/',Path.DirectorySeparatorChar)));if(!final.StartsWith(root,StringComparison.OrdinalIgnoreCase))throw new Exception("Unsafe archive path");paths[i]=final;}
  }
  if(!list){Directory.CreateDirectory(root);var cb=new Callback(paths);Marshal.ThrowExceptionForHR(arc.Extract(null,0xffffffff,0,cb));if(cb.Current!=null)cb.Current.F.Dispose();}
  arc.Close();ins.F.Dispose();return lines.ToArray();
 }
}
'@
[ArchiveRead]::Run('C:\Users\Test\AppData\Local\CapCut\Apps\8.8.0.3774\7z.dll',$InputArchive,$Destination,$Format,$ListOnly.IsPresent)
