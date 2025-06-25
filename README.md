Read setup.txt for the configuration

client_nxdomain_sender.py is for client side that will send info of nxdomain to server side
in this case local DNS will pass to BitRanger DNS

generate_bind_blockzones.py is located in the BitRanger DNS, it will generate A records for the indentified domain that are suspicious or known for malware website.
it helps DNS to redirect the domain to our local domain like picture shown

![image](https://github.com/user-attachments/assets/2126afba-1f70-46f2-b90e-e83d4a64fafd)

server_flask_dashboard.py will create the the dashboard showing all the nxdomain that has been looked up before or being resolve by what ip.
it will logs using bind logging, where all query will be logged in there
