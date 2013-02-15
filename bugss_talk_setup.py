#!/usr/bin/python
import ftputil,string,os,sys

#Where to put the genomes (script will create sub directories
#mirroring NCBI).  This directory must
#exist already:
base_path="."

host = ftputil.FTPHost('ftp.ncbi.nlm.nih.gov', 'anonymous', 'password')
host.chdir('/genomes/Bacteria/')

def dl(orgs): 
    exts = [".gbk",".fna",".ffn"]
    successes = []
    failures = []
    home_dirs = os.listdir('.')
    for org in orgs:
        print("Searching for " + org)
        host.chdir('/genomes/Bacteria/')
        dir_list = host.listdir(host.curdir)
        org_dirs = [dc for dc in dir_list if org in dc]
        #print(org_dirs)
        if not org_dirs:
            print("found nothing for " + org + ", moving on")
            failures.append(org)
            continue
        print("found " + str(len(org_dirs)) + " result" + "s" * (len(org_dirs) > 1))
        if len(org_dirs) > 1:
            for i,v in enumerate(org_dirs):
                print(i,v)
            print("choose a directory:")
            default= (filter(lambda d: org_matches_dir(org, d),home_dirs))
            if default:
                print("press (Enter) for default: %s" % default[0])
            choice = raw_input()
        else:
            choice = '0'
        dir_name = org_dirs[int(choice)] if len(choice) else default[0]
        #print(dir_name)
        host.chdir('/genomes/Bacteria/' + dir_name + '/')
        file_list = host.listdir(host.curdir)
        size_crit = lambda f: host.path.getsize(f)
        biggest = lambda ext: max([f for f in file_list
                                   if f.endswith(ext)],key=size_crit)
        biggest_files = [biggest(ext) for ext in exts]
        for file_name in biggest_files:
            if not os.path.isdir(os.path.join(base_path,dir_name)):
                print("Making directory " + os.path.join(base_path,dir_name))
                os.chdir(base_path)
                os.mkdir(os.path.join(base_path,dir_name))
                print(base_path,dir_name,file_name)
            if os.path.isfile(os.path.join(base_path,dir_name,file_name)):
                print("Skipping file "
                    + os.path.join(base_path,dir_name,file_name))
            elif host.path.isfile(file_name):
                print("Downloading file "
                    + os.path.join(base_path,dir_name,file_name))
                host.download(file_name, \
                                  os.path.join(base_path,dir_name,file_name), 't')
                successes.append(org)
            #Download arguments: remote filename, local filename, mode
            else:
                print("ERROR - Not a file " + dir_name + "/" + file_name)
    print("Summary:")
    print("Searched for %s organism" % len(orgs))
    print("Succeeded:")
    for success in successes:
        print(success)
    print("Failed:")
    for failure in failures:
        print(failure)
    if len(failures) == 0:
        print("None")

if __name__ == '__main__':
    dl(["Escherichia_coli_K_12_substr__MG1655"])
#    example usage:
#    dl(["Haemophilus_influenzae","Escherichia coli"])

