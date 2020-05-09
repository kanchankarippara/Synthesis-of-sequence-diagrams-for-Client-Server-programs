
import java.io.*; 
import java.net.*; 
import java.util.Scanner; 

//Client class 
public class EchoControlProtocol2 
{ 
	DataInputStream dis = null;
	DataOutputStream dos = null;
	public static void main(String[] args) throws Exception 
	{ 
		try
		{ 
			Scanner scn = new Scanner(System.in); 
			
			// getting localhost ip 
			InetAddress ip = InetAddress.getByName("localhost"); 
			

	
			// establish the connection with server port 5056 
			Socket s = new Socket(ip, 5056);
			String sock = null;

	
			// Writing port no to a string 
			sock = s.toString();
	
			// the following loop performs the exchange of 
			// information between client and client handler 
			while (true) 
			{ 
				DataInputStream dis = new DataInputStream(s.getInputStream());
				System.out.println(dis.readUTF()); 
				String tosend = scn.nextLine(); 
				DataOutputStream dos = new DataOutputStream(s.getOutputStream());
				dos.writeUTF(tosend); 
				
				// If client sends exit,close this connection 
				// and then break from the while loop 
				if(tosend.equals("Exit")) 
				{ 
					System.out.println("Closing this connection : " + s);
//					String sock1 = s.toString();
					s.close(); 
					System.out.println("Connection closed"); 
					break; 
				} 
				
				// printing date or time as requested by client 
				String received = dis.readUTF(); 
				System.out.println(received); 
			} 
			
			// closing resources 
			scn.close(); 
//			dis.close(); 
//			dos.close(); 
		}catch(Exception e){ 
			e.printStackTrace(); 
		} 
	} 
} 

