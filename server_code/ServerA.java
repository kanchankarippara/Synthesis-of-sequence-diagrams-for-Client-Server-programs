// Java implementation of Server side 
// It contains two classes : Server and ClientHandler 
// Save file as Server.java 

import java.io.*; 
import java.text.*; 
import java.util.*; 
import java.net.*; 

// Server class 
public class ServerA
{ 
	
	public static void main(String[] args) throws Exception 
	{ 
		// server is listening on port 5056 
		ServerSocket ss = new ServerSocket(5056); 
		
		// running infinite loop for getting 
		// client request 
		while (true) 
		{ 
			Socket s = null; 
			
			try
			{ 
				// socket object to receive incoming client requests 
				s = ss.accept();
				String sock = s.toString();
				
				System.out.println("A new client is connected : " + s); 
				
				// obtaining input and out streams 
				
				
				System.out.println("Assigning new thread for this client"); 

				// create a new thread object 
				Thread t = new ClientHandler(s); 

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
	DataInputStream dis = null; 
	DataOutputStream dos = null;

	final Socket s; 
	

	// Constructor 
	public ClientHandler(Socket s) throws Exception
	{ 
		this.s = s;  
	} 

	@Override
	public void run() 
	{ 
		String received; 
		String toreturn; 
		while (true) 
		{ 
			try { 

				// Ask user what he wants 
				DataOutputStream dos = new DataOutputStream(s.getOutputStream());
				dos.writeUTF("What do you want?[Date | Time]..\n"+ 
							"Type Exit to terminate connection."); 
				
				// receive the answer from client 
				DataInputStream dis = new DataInputStream(s.getInputStream()); 
				received = dis.readUTF(); 
				
				if(received.equals("Exit")) 
				{ 
					System.out.println("Client " + this.s + " sends exit...");
					String sock = s.toString();
					System.out.println("Closing this connection."); 
					this.s.close(); 
					System.out.println("Connection closed"); 
					break; 
				} 
				
				// creating Date object 
				Date date = new Date(); 
				
				// write on output stream based on the 
				// answer from the client 
				switch (received) { 
				
					case "Date" : 
						toreturn = fordate.format(date); 
						dos.writeUTF(toreturn); 
						break; 
						
					case "Time" : 
						toreturn = fortime.format(date); 
						dos.writeUTF(toreturn); 
						break; 
						
					default: 
						dos.writeUTF("Invalid input"); 
						break; 
				} 
			} catch (IOException e) { 
				e.printStackTrace(); 
			} 
		} 
		
//		try
//		{ 
//			// closing resources 
//			this.dis.close(); 
//			this.dos.close(); 
//			
//		}catch(Exception e){ 
//			e.printStackTrace(); 
//		} 
		 
		
	} 
} 
