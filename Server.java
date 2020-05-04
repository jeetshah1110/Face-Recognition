// Java implementation of Server side 
// It contains two classes : Server and ClientHandler 
// Save file as Server.java 

import java.io.*; 
import java.text.*; 
import java.util.*; 
import java.net.*; 

// Server class 
public class Server 
{ 
	public static void main(String[] args) throws IOException 
	{ 
		// server is listening on port 5056 
		ServerSocket ss = new ServerSocket(7800); 
		
		// running infinite loop for getting 
		// client request 
		while (true) 
		{ 
			Socket s = null; 
			
			try
			{ 
				// socket object to receive incoming client requests 
				s = ss.accept(); 
				
				System.out.println("A new client is connected : " + s); 
				
				// obtaining input and out streams 
				DataInputStream dis = new DataInputStream(s.getInputStream()); 
				DataOutputStream dos = new DataOutputStream(s.getOutputStream()); 
				
				System.out.println("Assigning new thread for this client"); 

				// create a new thread object 
				Thread t = new ClientHandler(s, dis, dos); 

				// Invoking the start() method 
				t.start(); 
				
			} 
			catch (Exception e){ 
				s.close(); 
				e.printStackTrace(); 
			} 
		} 
	} 
} 

// ClientHandler class 
class ClientHandler extends Thread 
{ 
	DateFormat fordate = new SimpleDateFormat("yyyy/MM/dd"); 
	DateFormat fortime = new SimpleDateFormat("hh:mm:ss"); 
	final DataInputStream dis; 
	final DataOutputStream dos; 
	final Socket s; 
	

	// Constructor 
	public ClientHandler(Socket s, DataInputStream dis, DataOutputStream dos) 
	{ 
		this.s = s; 
		this.dis = dis; 
		this.dos = dos; 
	} 

	@Override
	public void run() 
	{ 
		String FILE_TO_RECEIVED = "/home/shubham/FR/examples/MH10512.jpg";
		int FILE_SIZE = 6022386;
		String received; 
		String toreturn;
		int bytesRead;
    	int current = 0;
    	FileOutputStream fos = null;
    	BufferedOutputStream bos = null; 
		
			try { 
				received = dis.readUTF(); 
				
				//System.out.println("Filename Received");

				//receive File
				FILE_TO_RECEIVED = "/home/shubham/FR/examples/"+received+".jpg";
				
				
				 byte [] mybytearray  = new byte [FILE_SIZE];
      			 InputStream is = s.getInputStream();
     			 fos = new FileOutputStream(FILE_TO_RECEIVED);
      			 bos = new BufferedOutputStream(fos);
    		     bytesRead = is.read(mybytearray,0,mybytearray.length);
     			 current = bytesRead;

     			 do {
       		     bytesRead = is.read(mybytearray, current, (mybytearray.length-current));
                 if(bytesRead >= 0) current += bytesRead;
                  } while(bytesRead > -1);

     			 bos.write(mybytearray, 0 , current);
      			 bos.flush();
      		     System.out.println("File " + FILE_TO_RECEIVED + " downloaded (" + current + " bytes read)");
				
				//String file=dis.readUTF();
			
			//Process File
			
			System.out.println("Processing File");	
			
			 //send Result
			 
			 dos.writeUTF("File received");
			} catch (IOException e) { 
				e.printStackTrace(); 
			} 
		
		
		try
		{ 
			// closing resources 
			this.dis.close(); 
			this.dos.close(); 
			
		}catch(IOException e){ 
			e.printStackTrace(); 
		} 
	} 
} 

