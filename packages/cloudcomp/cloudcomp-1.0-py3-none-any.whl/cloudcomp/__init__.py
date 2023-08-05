

def index():
    print("""
Pract 1 
1a)  A client server based program using TCP to find if the number entered is prime.
1b) A client server TCP based chatting application.

Pract 2 
2a) A client server based program using UDP to find if the number entered is even or odd.
2b) A client server based program using UDP to find the factorial of the entered number.

Pract 3
3a) A program to implement simple calculator operations like addition, subtraction, multiplication and division using RPC.
3b) A program that finds the square, square root, cube and cube root of the entered number using RPC.

Pract 4
Implement Multicast Socket //pick any multicast addr within the range 224.0.0.0 to 239.255.255.255

Pract 5
5a) A RMI based application program to display current date and time.
5b) A RMI based application program that converts digits to words, e.g. 123 will be converted to one two three.

Pract 6
Show the implementation of Web Service.

Pract 7
Implementing Web Service that connects to MySQL database.    


""")
          



def prog(num):
    num = num.lower()
    if(num=="1a"):
        print(""" //TCP prime or not
              
import java.io.*;
import java.net.*;
import java.util.*;

public class Client {
    public static void main(String[] args) throws Exception{
        Socket cs = new Socket(InetAddress.getLocalHost(), 2000);
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        DataInputStream in = new DataInputStream(cs.getInputStream());
        DataOutputStream out = new DataOutputStream(cs.getOutputStream());
        
        System.out.println("Enter a number: ");
        String num = br.readLine();
        out.writeUTF(num);
        
        String res = in.readUTF();
        System.out.println("Result: "+res);
    }
}




import java.io.*;
import java.net.*;
import java.util.*;

public class Server {
    public static void main(String[] args) throws Exception {
        ServerSocket ss = new ServerSocket(2000);
        Socket s = ss.accept();
        DataInputStream in = new DataInputStream(s.getInputStream());
        DataOutputStream out = new DataOutputStream(s.getOutputStream());
        
        int num = Integer.parseInt(in.readUTF());
        
        String res = "Number is Prime";
        if(num == 0 || num == 1)
            res = "Number is not Prime";
        else if(num==2)
            res = "Number is Prime";
        else
            for(int i=2; i<=(num/2); i++)
                if(num%i == 0)
                    res = "Number is not Prime";
        
        out.writeUTF(res);
    }
}
             
              """)
        
    elif(num=="1b"):
        print(""" //TCP chatting application.
              
import java.io.*;
import java.net.*;
import java.util.*;

public class Client_3{
    public static void main(String[] args) throws Exception {
        Socket cs = new Socket(InetAddress.getLocalHost(), 2000);
        DataInputStream in = new DataInputStream(cs.getInputStream());
        DataOutputStream out = new DataOutputStream(cs.getOutputStream());
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        System.out.print("\-nClient Says: ");
        String message = br.readLine();
        out.writeUTF(message);
        while (true) {
            if(message.equalsIgnoreCase("exit"))
                break;
            String receive = in.readUTF();
            System.out.print("Server Says: "+receive);
            
            if(receive.equalsIgnoreCase("exit"))
                break;
            
            System.out.print("\-n\-nClient Says: ");
            String send = br.readLine();
            out.writeUTF(send);
            
            if(send.equalsIgnoreCase("exit"))
                break;
        }
        
    }
}



import java.io.*;
import java.net.*;
import java.util.*;

public class Server_3{
    public static void main(String[] args) throws Exception {
        ServerSocket ss = new ServerSocket(2000);
        Socket s = ss.accept();
        DataInputStream in = new DataInputStream(s.getInputStream());
        DataOutputStream out = new DataOutputStream(s.getOutputStream());
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        String message = in.readUTF();
        System.out.print("Client Says: "+message);
        
        while (true) {
            if(message.equalsIgnoreCase("exit"))
                break;
            System.out.print("\-nServer Says: ");
            String send = br.readLine();
            out.writeUTF(send);
            
            if(send.equalsIgnoreCase("exit"))
                break;
            
            String receive = in.readUTF();
            System.out.print("\-nClient Says: "+receive);
            
            if(receive.equalsIgnoreCase("exit"))
                break;

        }
        
    }
}
              
              """)
              
    elif(num=="2a"):
        print(""" // UDP Even odd
              
import java.io.*;
import java.net.*; 
import java.util.*; 


public class Client_3{
    public static void main(String[] args) throws Exception{
        DatagramSocket ds = new DatagramSocket(2000);
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        System.out.println("Eneter a number: ");
        String num = br.readLine();
        
        byte[] b = num.getBytes();
        DatagramPacket dp = new DatagramPacket(b, b.length, InetAddress.getLocalHost(), 1000);
        ds.send(dp);
        
        byte[] b2 = new byte[1024];
        DatagramPacket dp2 = new DatagramPacket(b2, b2.length);
        ds.receive(dp2);
        
        String res = new String(dp2.getData(),0,dp2.getLength());
        System.out.println(res);
        
    }
}

import java.io.*;
import java.net.*; 
import java.util.*; 

public class Server_3{
    public static void main(String[] args) throws Exception {
        DatagramSocket ds = new DatagramSocket(1000);
        
        byte[] b = new byte[1024];
        DatagramPacket dp = new DatagramPacket(b, b.length);
        ds.receive(dp);
        int num = Integer.parseInt(new String(dp.getData(),0,dp.getLength()) );
        
        String res = "";
        if(num%2==0)
            res = "Number is Even";
        else
            res = "Number is Odd";
        
        byte[] b2 = res.getBytes();
        DatagramPacket dp2 = new DatagramPacket(b2, b2.length, InetAddress.getLocalHost(), 2000);
        ds.send(dp2);
           
    }
}
            
              """)
              
    elif(num=="2b"):
        print(""" //UDP Fact
              
import java.io.*;
import java.net.*;
import java.util.*;

 public class Client_3{
    public static void main(String[] args) throws Exception{
        DatagramSocket ds = new DatagramSocket(2000);
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        System.out.println("Enter a number");
        String num = br.readLine();
        
        byte[] b = num.getBytes();
        DatagramPacket dp = new DatagramPacket(b, b.length, InetAddress.getLocalHost(), 1000);
        ds.send(dp);
        
        byte[] b2 = new byte[1024];
        DatagramPacket dp2 = new DatagramPacket(b2, b2.length);
        ds.receive(dp2);
        String res = new String(dp2.getData(),0,dp2.getLength());
        System.out.println(res);
    }
}    

import java.io.*;
import java.net.*;
import java.util.*;

public class Server_3{
    public static void main(String[] args) throws Exception{
        DatagramSocket ds = new DatagramSocket(1000);
        
        byte[] b = new byte[1024];
        DatagramPacket dp = new DatagramPacket(b, b.length);
        ds.receive(dp);
        
        int num = Integer.parseInt(new String(dp.getData(),0,dp.getLength()));
        int fact = 1;
        for(int i=1; i<=num; i++)
            fact = fact*i;
        
        String res = "Factorial of the given number is "+fact;
        byte[] b2 = res.getBytes();
        DatagramPacket dp2 = new DatagramPacket(b2, b2.length, InetAddress.getLocalHost(), 2000);
        ds.send(dp2);
            
    }
}         
              """)
        
    elif(num=="3a"):
        print(""" //RPC Calculator
              
import java.io.*;
import java.net.*;
import java.util.*;

public class Client_3{
    public static void main(String[] args) throws Exception{
        DatagramSocket ds = new DatagramSocket(2000);
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        System.out.println("Enter the operation you want to perform ");
        System.out.println("Example: add 1 2 or sub 5 3 or mul 2 3 or div 4 2");
        String op = br.readLine();
        
        byte[] b = op.getBytes();
        DatagramPacket dp = new DatagramPacket(b, b.length, InetAddress.getLocalHost(), 1000);
        ds.send(dp);
        
        byte[] b2 = new byte[1024];
        DatagramPacket dp2 = new DatagramPacket(b2, b2.length);
        ds.receive(dp2);
        String res = new String(dp2.getData(),0,dp2.getLength());
        System.out.println(res);
    }
}  


import java.io.*;
import java.net.*;
import java.util.*;


public class Server_3{
    public static void main(String[] args) throws Exception{
        DatagramSocket ds = new DatagramSocket(1000);
        
        byte[] b1 = new byte[1024];
        DatagramPacket dp = new DatagramPacket(b1, b1.length);
        ds.receive(dp);
        String op = new String(dp.getData(),0,dp.getLength());
        
        StringTokenizer st = new StringTokenizer(op, " ");
        String method = st.nextToken();
        int num1 = Integer.parseInt(st.nextToken());
        int num2 = Integer.parseInt(st.nextToken());
        String res = "--";
        
        if(method.equalsIgnoreCase("add"))
            res = "Result of the Operation is: " + add(num1,num2);
        else if(method.equalsIgnoreCase("sub"))
            res = "Result of the Operation is: " + sub(num1,num2);
        else if(method.equalsIgnoreCase("mul"))
            res = "Result of the Operation is: " + mul(num1,num2);
        else if(method.equalsIgnoreCase("div"))
            res = "Result of the Operation is: " + div(num1,num2);
        else
            res = "Invalid operation";
        
        byte[] b2 = res.getBytes();
        DatagramPacket dp2 = new DatagramPacket(b2, b2.length, InetAddress.getLocalHost(), 2000);
        ds.send(dp2);
    }
    
    public static int add(int a , int b){ return a + b ;}
    public static int sub(int a , int b){ return a - b ;}
    public static int mul(int a , int b){ return a * b ;}
    public static int div(int a , int b){ return a / b ;} 
}
           
              """)
              
    elif(num=="3b"):
        print(""" //RPC sq sqrt
              
import java.io.*;
import java.net.*;
import java.util.*; 

public class Client_3{
    public static void main(String[] args) throws Exception {
        DatagramSocket ds = new DatagramSocket(2000);
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        System.out.println("Enter the operation you want to perform ");
        System.out.println("Example: sq 2 or sqrt 9 or cube 3 or cbrt 27 ");
        String op = br.readLine();
        byte[] b = op.getBytes();     
        DatagramPacket dp = new DatagramPacket(b, b.length,InetAddress.getLocalHost(), 1000);
        ds.send(dp);
        
        byte[] b2 = new byte[1024];     
        DatagramPacket dp2 = new DatagramPacket(b2, b2.length);
        ds.receive(dp2);
        String res = new String(dp2.getData(),0,dp2.getLength());
        
        System.out.println("Result: "+res);
        
    }
}


import java.io.*;
import java.net.*;
import java.util.*; 

public class Server_3{
    public static void main(String[] args) throws Exception {
        DatagramSocket ds = new DatagramSocket(1000);
        
        byte[] b = new byte[1024];     
        DatagramPacket dp = new DatagramPacket(b, b.length);
        ds.receive(dp);
        
        String op = new String(dp.getData(),0,dp.getLength());
        StringTokenizer st = new StringTokenizer(op);
        String method = st.nextToken();
        double num = Double.parseDouble(st.nextToken());
        
        String res = "";
        if(method.equalsIgnoreCase("sq"))
            res = ""+sq(num);
        if(method.equalsIgnoreCase("sqrt"))
            res = ""+sqrt(num);
        if(method.equalsIgnoreCase("cube"))
            res = ""+cube(num);
        if(method.equalsIgnoreCase("cbrt"))
            res = ""+cbrt(num);
        
        byte[] b2 = res.getBytes();     
        DatagramPacket dp2 = new DatagramPacket(b2, b2.length,InetAddress.getLocalHost(), 2000);
        ds.send(dp2);
        
        
        
    }
    public static double sq(double n){return n*n;}
    public static double sqrt(double n){return Math.sqrt(n);}
    public static double cube(double n){return n*n*n;}
    public static double cbrt(double n){return Math.cbrt(n);}
}

            
              """)

    elif(num=="4"):  ################# (PENDING!!!) ###########
        print(""" 
              
              """)
              
    elif(num=="5a"):
        print(""" //RMI Date

//InterDate.java
import java.rmi.*;
public interface InterDate extends Remote {
    public String display() throws RemoteException;
}



//RMIClient.java
import java.rmi.*;
import java.rmi.server.*;
import java.rmi.registry.*;

public class RMIclient {
     public static void main(String[] args) {
        try{
            Registry reg = LocateRegistry.getRegistry("localhost",8000);
            String s1;
            InterDate h1 = (InterDate)reg.lookup("DS");
            s1 = h1.display();
            System.out.println(s1);
        }
        catch(NotBoundException | RemoteException e){
            System.out.println("Exception"+e);
        }
    }
}



//RMIServer.java
import java.rmi.*;
import java.rmi.registry.*;
import java.rmi.server.*;
import java.util.*;

public class RMIserver  extends UnicastRemoteObject implements InterDate {
public RMIserver() throws RemoteException {}
  public String display() throws RemoteException {
    String str = "";
    Date d=new Date();
    str=d.toString();
    return str;
}
    public static void main(String args[]) throws RemoteException {
    try{
        Registry reg = LocateRegistry.createRegistry(8000);
        RMIserver s1 = new RMIserver();
        reg.rebind("DS", s1);
        System.out.println("Object registered...");
    }
    catch(RemoteException e){
        System.out.println("Exception:"+e);
    }
  }
}
              
              
              
              """)


    elif(num=="5b"):
        print(""" //RMI Convert
              
//InterConvert.java
import java.rmi.*;
public interface InterConvert extends Remote{
     public String convertDigit(String no) throws RemoteException;
}   



//ClientConvert.java
import java.io.*;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class ClientConvert {
    public static void main(String[] args) {
        try{
            Registry reg = LocateRegistry.getRegistry("localhost",9000);
            String s1;
            InterConvert h1 = (InterConvert)reg.lookup("Wrd");
            BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
            System.out.println("Enter a number : \t"); 
            String no = br.readLine();
            s1 = h1.convertDigit(no);
            System.out.println("After Conversion: "+s1);
        }
        catch(Exception e){
            System.out.println("Exception: "+e);
        }
    }
} 



//ServerConvert.java
import java.rmi.*;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.*;
public class ServerConvert extends UnicastRemoteObject implements InterConvert{
    public ServerConvert() throws RemoteException {}
    public String convertDigit(String no) throws RemoteException {
        String str = "";
        for(int i = 0; i < no.length(); i++) {
            int p = no.charAt(i);
            if( p == 48)
                str += "zero ";
            if( p == 49)
                str += "one ";
            if( p == 50)
                str += "two ";
            if( p == 51)
                str += "three ";
            if( p == 52)
                str += "four ";
            if( p == 53)
                str += "five ";
            if( p == 54)
                str += "six ";
            if( p == 55)
                str += "seven ";
            if( p == 56)
                str += "eight ";
            if( p == 57)
                str += "nine ";
        }
        return str;
    }
    public static void main(String args[]) throws RemoteException
    {
        try{
            Registry reg = LocateRegistry.createRegistry(9000);
            ServerConvert s1 = new ServerConvert();
            reg.rebind("Wrd",  s1);
            System.out.println("Object registered...");
        }       
        
        catch(RemoteException e){
            System.out.println("Exception:"+e);
        }
    }
}          
              
              
              """)
              
    elif(num=="6"):
        print(""" 
              
              """)


    elif(num=="7"):
        print(""" 
              
              """)

    else:
        print(""" Invalid Input """)



    
    


















