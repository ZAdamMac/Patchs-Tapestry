# Tapestry Backup Automation Tool
# Coded in python3 at Patch Savage Labs
# git: ~/ZAdamMac/Patchs-Tapestry
global version; version = "DevBuild"  # Sets the version to display. "DevBuild" enables some extra debugging not normally accessable

# Importing Modules
import argparse
import configparser
import datetime
import gnupg
import math
import multiprocessing as mp
import os
import os.path
import pickle
import platform
import shutil
import tarfile


# Defining Classes
class skipLogger:  # dedicated skip-logging handler for use in buildBlocks
    def __init__(self, landingdir,
                 name):  # starts the skiplogger and tells it it will be writing to landingdir with name
        landingAbs = os.path.join(landingdir, name)
        if not os.path.exists(landingdir):
            os.makedirs(landingdir)
        self.loggerfile = open(landingAbs, "w")  # This will REPLACE the existing logfile with the new one so BE FUCKING CAREFUL
        self.loggerfile.write("The files in the following locations were excluded from the most recent backup. \n")
        self.loggerfile.write("This was due to their filesize exceeding the configured blocksize limit. \n")
        self.loggerfile.write("\n")

    def log(self, foo):  # Formats foo nicely and adds it to the log
        self.loggerfile.write(foo + '\n')

    def save(self):  # saves the file to disk. Once used you have to re-instance the logger
        self.loggerfile.write("\n")
        self.loggerfile.write("\n This backup was run on " + str(date.today()))
        self.loggerfile.flush()
        self.loggerfile.close()


class tapBlock(object):
    def __init__(self, size, label):
        self.sizeCur = 0
        self.sizeMax = size
        self.label = label
        self.full = False
        self.contents = {}

    def add(self, FID, fSize, fPath):  # General function for adding a file to the box. Called during block assembly.
        if (self.sizeMax - self.sizeCur) > smallest:
            self.full = True
            return "full"
        if fSize > (self.sizeMax - self.sizeCur):  # Handling for files larger than will fit in the current block
            return "pass"
        if fSize <= (self.sizeMax - self.sizeCur):  # This file fits
            self.contents.update({FID: fPath})
            self.sizeCur += fSize
            return "stored"

    def pack(self):  # enques the contents of the block for packaging
        os.chdir(drop)
        for file in self.contents:
            tasks.put(buildTasker("tar", self.label, file, self.contents[file]))
        if self.label.endswith("1.tap"):
            tasks.put(buildTasker("tar", self.label, "recovery.pkl", pathPickle))


class tapProc(mp.Process):
    def __init__(self, qTask):
        mp.Process.__init__(self)
        self.qTask = qTask
        os.chdir(drop)

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.qTask.get()
            if next_task is None:
                debugPrint('%s: Exiting' % proc_name)
                self.qTask.task_done()
                break
            next_task()
            self.qTask.task_done()
        return


class buildTasker(object):
    def __init__(self, tarfile, a, b):
        self.tarf = tarfile
        self.a = a  # TAR:FID
        self.b = b  # TAR: PATH

    def __call__(self):
        tar = tarfile.open(self.tarf, "w:bz2")
        tar.add(self.b, arcname=self.a)
        tar.close()

        if self.step == "sig":
            with open(self.tarf, "r") as p:
                sig = gpg.sign_file(p, keyid=self.a, output=tgt, detach=True, passphrase=str(self.b))


class encTasker(object):
    def __init__(self, tarfile, fp):
        self.tarf = tarfile
        self.fp = fp

    def __call__(self):
        with open(self.tarf, "r") as p:
            tgtOutput = os.path.join(drop, tar)
            debugPrint("Encrypting - sending block to: " + tgtOutput)
            k = gpg.encrypt_file(p, fp, output=tgtOutput, armor=True, always_trust=True)
            if k.ok == True:
                debugPrint("Success.")
            elif k.ok == False:
                debugPrint(str(k.status))


class sigTasker(object):
    def __init__(self, block, sigfp):
        self.block = block
        self.fp = sigfp

    def __call__(self):
        with open(self.block, "r") as p:
            tgtOutput = block + ".sig"
            debugprint("Signing: " + tgtOutput)
            sis = gpg.sign_file(p, keyid=self.fp, output=tgtOutput, detach=True, passphrase=ns.secret)
            if sis.ok == True:
                debugPrint("Success.")
            elif sis.ok == False:
                debugPrint(str(sis.status))


class recTask(object):
    def __init__(self, tar, fid, catdir, pathend):
        self.tar = tar
        self.fid = fid
        self.catdir = catdir
        self.pathend = pathend

    def __call__(self):
        absTar = os.path.join(workDir, self.tar)
        placementEnd, nameProper = os.path.split(
            self.pathend)  # split the pathend component into the subpath from the category dir, and the original filename.
        placement = os.path.join(self.catdir, placementEnd)  # merges the subpath and the category path
        with tarfile.open(absTar, "r:bz2") as tf:
            tf.extract(self.fid, path=placement)  # the file is now located where it needs to be.
        placed = os.path.join(placement, self.fid)
        os.rename(placed, proper)  # and now it's named correctly.


class recProc(mp.Process):
    def __init__(self, qTask):
        mp.Process.__init__(self)
        self.qTask = qTask
        os.chdir(drop)

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.qTask.get()
            if next_task is None:
                # Poison pill means shutdown
                debugPrint('%s: Exiting' % proc_name)
                self.qTask.task_done()
                break
            next_task()
            self.qTask.task_done()
        return


# Defining all functions!
def debugPrint(foo):
    if ns.debug:
        print(str(foo))


def announce():
    if __name__ = "__main__":
        print("Welcome to Tapestry Backup Tool Version " + version)


def init():
    print("Configuration file not found.")
    print("Beginning first-time setup.")
    print("To begin with, please provide your username on this system.")
    uid = raw_input("Username:")
    config.set("Environment Variables", "uid", str(uid))
    print("Next, enter a label to uniquely identify this computer.")
    compID = raw_input("CompID:")
    config.set("Environment Variables", "compID", str(compID))
    print("Please enter the desired blocksize in MB.")
    blockSize = raw_input("(4000)")
    config.set("Environment Variables", "compID", blockSize)
    print("If you have a signing key you wish to use, please enter it, else 0.")
    sigFP = raw_input("FP: ")
    config.set("Environment Variables", "signing fp", str(sigFP))
    if sigFP != "0":
        config.set("Environment Variables", "sign by default", str(True))
    else:
        config.set("Environment Variables", "sign by default", str(False))
    print("Excellent. Tapestry will now create a default configuration file here:")
    print(str(homeDir))
    config.set("Default Locations/Nix", "Docs", "/home/" + uid + "/Documents")
    config.set("Default Locations/Nix", "Photos", "/home/" + uid + "/Pictures")
    config.set("Additional Locations/Nix", "Video", "/home/" + uid + "/Videos")
    config.set("Additional Locations/Nix", "Music", "/home/" + uid + "/Music")
    config.set("Default Locations/Win", "Docs", "C:/Users/" + uid + "/My Documents")
    config.set("Default Locations/Win", "Photos", "C:/Users/" + uid + "/My Pictures")
    config.set("Additional Locations/Win", "Video", "C:/Users/" + uid + "/My Videos")
    config.set("Additional Locations/Win", "Music", "C:/Users/" + uid + "/My Music")
    print("Please review this file. If you need to make any changes to the included backup")
    print("locations, please run the program again with the flag --setup.")
    with open("tapestry.cfg", "w") as cfg:
        config.write(cfg)
    exit()


def checkGPGConfig():
    if signing:  # if signing is disabled by default we don't care about loopback pinentry because a DR key doesn't use a passphrase
        tgt = gpgDir + "/gpg-agent.conf"
        with open(tgt, "rw") as conf:
            for line in conf:
                if "allow-loopback-pinentry" in line:
                    configured = true
                    break
        if not configured:
            print("Tapestry has detected that loopback pintentry is disabled in your gpg installation.")
            print("Tapestry can enable this function, but doing so carries security risks. See the readme.")
            print("Press enter to accept these risks, or control-c to cancel.")
            conf.write("allow-loopback-pinentry")
            conf.close()
        else:
            conf.close()


def setup():
    global setupMode
    setupMode = True
    print("Entering the setup menu")
    while setupMode:
        print("Please Select from the following options:")
        print("1. Change User ID")
        print("2. Change Machine Label")
        print("3. Change Block Size")
        print("4. Directory Management")
        print("5. Key Options")
        print("6. Quit")
        func = raw_input("Option:")
        if func == "1":
            print("Please enter the desired username.")
            uid = raw_input("Username:")
            config.set("Environment Variables", "uid", str(uid))
            print("New UID Set: " + uid)
        elif func == "2":
            print("The current machine label is: " + str(config.getopt("environment Variables", "compID")))
            print("Please enter the new label.")
            compID = raw_input("Machine Label:")
            config.set("Environment Variables", "compID", str(compID))
            print("The new label was set to :" + compID)
        elif func == "3":
            print("The Blocksize determines the maximum size in MB a .tap block can be.")
            print("It is recommended to choose a value 100 MB less than the capacity of your media.")
            print("Please enter a new blocksize in MB.")
            newSize = raw_input("Default is 4000:")
            config.set("Environment Variables", "blockSize", newSize)
        elif func == "4":
            print("The directory management function is under construction.")
            print("Your configuration file is at:")
            locationConfig = os.path.join(homeDir, "tapestry.cfg")
            print(str(locationConfig))
            print("Please edit this file directly to add, remove, or change target directories and their labels.")
        elif func == "5":
            print("Tapestry can sign your blocks for you, to prevent tampering.")
            if signing:
                print("Default signing is currently on.")
            else:
                print("Default signing is currently off.")
            print("Blocks will be signed with the key with the following fingerprint:")
            print(str(sigFP))
            print("You can:")
            print("1. Toggle Default Signing")
            print("2. Assign a new signing key")
            print("3. Toggle Keyring Mode.")
            print("4. Go Back")
            subfunc = raw_input("Choice?")
            if subfunc == "1":
                if signing:
                    signing = False
                    config.set("Environment Variables", "sign by default", str(False))
                else:
                    signing = True
                    config.set("Environment Variables", "sign by default", str(True))
            elif subfunc == "2":
                print("Please enter the fingerprint of the new key.")
                sigFP = raw_input("FP: ")
                config.set("Environment Variables", "signing fp", str(sigFP))
            elif subfunc == "3":
                if not keyringMode:
                    keyringMode = True
                    config.set("Environment Variables", "keyringMode", str(True))
                else:
                    keyringMode = False
                    config.set("Environment Variables", "keryingMode", str(False))
            else:
                pass
        elif func == "6":
            print("Exiting Setup.")
            setupMode = False
            with open("tapestry.cfg", "w") as cfg:
                config.write(cfg)
        else:
            print("Your entry was not a valid option.")
            print("Please enter the number of the option you wish to execute.")


def findKeyFile(arg):
    foundKey = False
    if not keyringMode:
        if arg == "pub":
            tgt = "DRPub.key"
        elif arg == "sec":
            tgt = "DR.key"
        if currentOS == "Linux":
            dirSearch = ("/media/" + uid)
            for root, dirs, files in os.walk(dirSearch):
                for file in files:
                    if file == tgt:
                        foundKey = True
                        pathKey = os.path.join(root, tgt)
                        debugPrint("Found key at: " + pathKey)
        if currentOS == "Windows":
            drives = ['{}:\\' for letter in 'DEFGHIJKLMNOPQRSTUVWXYZ']
            for drive in drives:
                if os.path.isdir(drive):
                    for root, dirs, files in os.walk(drive):
                        for file in files:
                            if file == tgt:
                                foundKey = True
                                pathKey = os.path.join(root, tgt)
                                debugPrint("Found key at: " + pathKey)
                if foundKey == True:
                    break
    else:
        print("Tapestry will use the key with the fingerprint %s for this session." % expectedFP)

    if not foundKey:
        if not keyringMode:
            print("No key found, beginning new key generation. Press ctrl+c to cancel.")
            getPassphrase = True
            while getPassphrase:
                print("Please enter a passphrase to protect this recovery key. Leave blank to skip.")
                s1 = input(">")
                if s1 != None:
                    print("Please enter the passphrase again.")
                    s2 = input(">")
                    if s1 == s2:
                        secret = s1
                        break
                    else:
                        pass
                else:
                    secret = None
                    getPassphrase = False
            print("Generating a new recovery key, please stand by.")
            input_data = gpg.gen_key_input(key_type="RSA", key_length=2048, name_real=str(uid),
                                           name_comment="Disaster Recovery", name_email="nul@autogen.key",
                                           passphrase=secret)
            keypair = gpg.gen_key(input_data)
            debugPrint(keypair.fingerprint)
            fp = keypair.fingerprint  # Changes the value of FP to the new key
            config.set("Environment Variables", "Expected FP", str(fp))  # sets this value in config
            with open("tapestry.cfg", "w") as cfg:
                config.write(cfg)
            if not os.path.isdir(drop):
                os.mkdir(drop)
            os.chdir(drop)
            pubOut = gpg.export_keys(fp)
            keyOut = gpg.export_keys(fp, True)
            pubFile = os.open("DRPub.key", os.O_CREAT | os.O_RDWR)
            pubHandle = os.fdopen(pubFile, "w")
            pubHandle.write(str(pubOut))
            pubHandle.close()
            keyFile = os.open("DR.key", os.O_CREAT | os.O_RDWR)
            keyHandle = os.fdopen(keyFile, "w")
            keyHandle.write(str(keyOut))
            keyHandle.close()
            print("The exported keys have been saved in the output folder. Please move them to removable media.")


def loadKey():
    global activeFP
    debugPrint("loadkey Start")
    if not keyringMode:
        foo = input("Press enter to confirm that the system will use the key located at " + pathKey)
        keyFile = open(pathKey)
        keyData = keyFile.read()
        importResult = gpg.import_keys(keyData)
        debugPrint("I have imported key: " + importResult.fingerprints[0])
        debugPrint("I was expecting: " + expectedFP)
        if str(importResult.fingerprints[0]) != expectedFP:
            print(
                "WARNING: the fingerprint of the DR key imported from the supplied thumb drive does not match the expected value.")
            print("This could pose a threat to the privacy of your backups.")
            print("If this is acceptable, type OK to continue. Your expected FP value will be changed.")
            confirmation = input("OK?")
            if confirmation == "OK":
                debugPrint("Setting the new expected fp to %s" % str(importResult.fingerprints[0]))
                config.set("Environment Variables", "expected fp", str(importResult.fingerprints[0]))
                with open("tapestry-test.cfg", "w") as cfg:  # TODO detest
                    config.write(cfg)
            else:
                print("You have indicated you do not wish to use the current key. The program will now terminate.")
                remKey()
                exit()
        debugPrint(str(importResult.count) + " keys imported.")
        print("Key imported. If program terminates irregularly, remove manually from GPG.")
        activeFP = importResult.fingerprints[0]

    if keyringMode:
        debugPrint("Fetching key from Keyring")
        activeFP = expectedFP
        debugPrint(activeFP)


def createDIRS():
    if currentOS == "Linux":
        workDir = "

    if not os.path.exists(workDir):
        os.mkdir(workDir)
    if not os.path.exists(drop):
        os.mkdir(drop)


def findblock():  # Time to go grepping for taps!
    os.chdir(media)
    for foo, bar, files in os.walk(media):
        for file in files:
            if file.endswith(".tap"):
                os.chdir(os.path.join(a + media))
                global foundBlock;
                foundblock = file


def validateBlock():
    print("Checking the validity of this disk's signature.")
    global valid
    for dont, care, files in os.walk(media):
        for file in files:
            debugPrint("Looking for a sig at file: " + file)
            if file.endswith(".sig"):
                sig = os.path.join(dont, file)
            elif file.endswith(".tap"):
                data = os.path.join(dont, file)
            else:
                continue
    if sig == None:
        print("No signature is available for this block. Continue?")
        go = raw_input("y/n?")
        if go.lower() == "y":
            valid = True
        else:
            print("Aborting backup.")
            clearDown()
            exit()
    else:
        with open(sig) as fsig:
            verified = gpg.verify_file(fsig, data)
        if verified.trust_level is not None and verified.trust_level >= verified.TRUST_FULLY:
            valid = True
            print("This block has been verified by %s, which is sufficiently trusted." % verified.username)
        else:
            print("This block claims to have been signed by %s." % verified.username)
            print("The signature is %s. Continue?" % verified.trust_text)
            go = raw_input("y/n?")
            if go.lower() == "y":
                valid = True
            else:
                print("Aborting backup.")
                clearDown()
                exit()


def decryptBlock():
    global foundBlock
    os.mkdir(os.path.join(workDir, foundBlock))
    outputTGT = str(os.path.join(workDir, foundBlock))
    with open(a + "/" + file, "r") as kfile:
        if secret == None:
            baz = gpg.decrypt_file(kfile, output=outputTGT, always_trust=True)
        else:
            baz = gpg.decrypt_file(kfile, output=outputTGT, always_trust=True, passphrase=secret)
        if not baz.ok:
            debugPrint("Decryption Error: " + str(baz.status))


def openPickle():
    for foo, bar, files in os.walk(workDir):
        for file in files:
            if file.endswith("1.tap"):
                with tarfile.open(os.path.join(foo, file), "r:bz2") as tfile:
                    tfile.extract("recovery.pkl", path=workDir)
    for a, b, files in os.walk(workDir):
        for file in files:
            if file == "recovery.pkl":
                foo = os.path.join(a, file)
                global recPaths
                global recSections
                global numVolumes
                listRecovery = pickle.load(open(foo))
                numVolumes, recPaths, recSections = listRecovery
    if len(
            recPaths) > 0:  # Throws an internal error if the required files are not properly mounted and closes the program so that it will not damage the archive
        print("Found Recovery Table 1")
    else:
        print(
            "There was a problem finding the file 'recPaths' on the disk. Please reload this program and try again, being careful to use Disk 1.")
        clearDown()  # Deletes temporary files to prevent system bloat
        remKey()  # removes the recovery secret key from the keyring per protocol
        exit()
    if len(recSections) > 0:
        print("Found Recovery Table 2")
    else:
        print(
            "There was a problem finding the file 'recovery.pkl' on the disk. Please reload this program and try again, being careful to use Disk 1.")
        clearDown()
        remKey()
        exit()


def unpackBlocks():
    global tasker
    tasker = mp.joinableQueue()
    for foo, bar, files in os.walk(workDir):
        for file in files:
            if file.endswith(".tap"):
                with tarfile.open(os.path.join(foo, file), "r:bz2")as tf:
                    for item in tf.getnames():  # at this point item yields a tap FID
                        cat = recSections[item]
                        try:
                            catdir = dirActual[cat]
                        except KeyError:
                            catdir = os.path.join(drop, cat)
                        pathend = recPaths[item]
                        tasker.put(rectask(file, fid, catdir, pathend))
    for foo in range(numConsumers):
        tasker.put(None)  # seed poison pills at the end of the queue to kill the damn consumers


def rmkey():
    if not keyringMode:
        gpg.delete_keys(fp, True)
        gpg.delete_keys(fp)
        print("The recovery key has been deleted from the keyring.")


def cleardown():
    if os.path.exists(workDir):
        shutil.rmtree(workDir)
    rmkey()


def getContents(category, tgt):
    print("Currently walking the " + category + " directory.")
    for fromRoot, dirs, files, in os.walk(str(tgt)):
        for item in files:
            global sumSize
            global counterFID
            global listSection
            foo = counterFID + 1
            counterFID = foo
            metaTGT = os.path.join(fromRoot, item)
            size = os.path.getsize(metaTGT)
            fooSize = sumSize + size
            sumSize = fooSize
            listAbsolutePaths.update({str(counterFID): str(metaTGT)})
            listFSNames.update({str(counterFID): str(item)})
            listSizes.update({str(counterFID): str(size)})
            relativePath = metaTGT.replace(tgt, "~",
                                           1)  # removes tgt from the path string, leaving the path string after the root of TGT, including subfolders, for recovery.
            listRelativePaths.update({str(counterFID): str(relativePath)})
            listSection.update({str(counterFID): str(category)})
    debugPrint("After crawling " + category + " there are " + str(len(listAbsolutePaths)) + " items in the index.")


def makeIndex():  # does some operations to the working dictionaries to remove items that are too large and place them in order.
    print("Compiling the working indexes")
    global workIndex
    workIndex = sorted(listSizes, key=listSizes.__getitem__)
    workIndex.reverse()  # yields the index sorted by descending file size.
    for item in workIndex:  # We need to remove the largest items.
        size = int(listSizes[item])
        if size > blockSizeActual:
            print("Error: %s is too large to be processed and will be excluded." % listFSNames[item])
            skiplogger.log(listAbsolutePaths[item])
            workIndex.delete(item)
    global smallest
    smallest = int(workIndex[(len(workIndex) - 1)])


def buildBlocks():
    print("Beginning the blockbuilding process. This may take a moment.")
    numBlocks = math.ceil(sumSize / blockSizeActual)
    for i in range(numBlocks):
        SID = str(str(compid) + str(date) + str(i) + ".tap")
        blocks.append(tapBlock(blockSizeActual, SID))
    for block in blocks:
        debugPrint("Testing in Block: " + str(block))
        if block.full == False:
            for FID in workIndex:
                fSize = listSizes[FID]
                status = block.add(FID, fSize, listAbsolutePaths[FID])
                if status == "pass":
                    continue
                elif status == "stored":
                    workIndex.delete(FID)
        if len(workIndex) == 0:
            break
    print("There are no items left to sort.")
    placePickle()


def placePickle():  # generates the recovery pickle and leaves it where it can be found later.
    os.chdir(workDir)
    global sumBlocks
    sumBlocks = len(blocks)
    listRecovery = [sumBlocks, listRelativePaths,
                    listSection]  # Believe it or not, this number and these two lists are all we need to recover from a tapestry backup!
    recPickle = os.open("recovery.pkl", os.O_CREAT | os.O_RDWR)
    filePickles = os.fdopen(recPickle, "wb")
    pickle.dump(listRecovery, filePickles)


def processBlocks():  # signblocks is in here now
    print("Packaging Blocks.")
    debugPrint("Spawning %s processes." % numConsumers)
    if signing:
        global secret
        secret = input("Please enter the passphrase/pin for the signing key now.")
    if __name__ == '__main__':
        os.chdir(homeDir)
        global blocks
        mp.set_start_method("spawn")
        tasks = mp.JoinableQueue()
        consumers = []
        for i in range(numConsumers):
            consumers.append(tapProc(tasks))
        for b in blocks:
            b.pack()
        for w in consumers:
            w.start()
        tasks.join()
        for foo, bar, blocks in os.walk(drop):
            for block in blocks:
                if block.endswith(".tap"):
                    tasks.put(buildTasker("enc", block, activeFP, None))
        tasks.join()
        for w in consumers:
            tasks.put(None)
        tasks.join()
        debugPrint("End of processBlocks()")


def buildMaster():  # summons the master process and builds its corresponding namespace, then assigns some starting values
    if __name__ == "__main__":
        master = mp.Manager()
        ns = master.Namespace()

        ns.os = platform.system()  # replaces old global var currentOS
        ns.date = datetime.date()
        ns.home = os.getcwd()
        ns.numConsumers = len(
            os.sched_getaffinitiy(0))  # The practical limit of consumer processes during multiprocessed blocks.
        ns.secret = None  # Placeholder so that we can use this value later as needed. Needs to explicitly be none in case no password is used.


def parseArgs():  # mounts argparser, crawls it and then assigns to the managed namespace
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Automatically backup or restore personal files from the system.")
        parser.add_argument('--rcv', help="Recover a previous archive from disk.", action="store_true")
        parser.add_argument('--setup', help="Loads the program in user configuration mode", action="store_true")
        parser.add_argument('--inc', help="Tells the system to include non-default sections in the backup process.",
                            action="store_true")
        parser.add_argument('--debug', help="Increase output verbosity.", action="store_true")
        args = parser.parse_args()

        ns.rcv = args.rcv
        ns.setup = args.setup
        ns.inc = args.inc
        ns.debug = args.debug


def parseConfig():  # mounts the configparser instance, grabs the config file, and passes its values into the namespace
    if __name__ == "__main__":
        config = configparser.SafeConfigParser()
        if version == "DevBuild":
            cfg = "tapestry-test.cfg"
        else:
            cfg = "tapestry.cfg"

        if os.path.exists(os.getcwd() + "/" + cfg):
            config.read(cfg)
            uninit = False
        else:  # the finished version should include a tapestry.cfg file by default for clarity, but in a pinch we can assign some defaults.
            uninit = True
            config.add_section("Environment Variables")
            config.add_section("Default Locations/Nix")
            config.add_section("Additional Locations/Nix")
            config.add_section("Default Locations/Win")
            config.add_section("Additional Locations/Win")
            config.set("Environment Variables", "blockSize", "4000")
            config.set("Environment Variables", "expected fp", "0")
            config.set("Environment Variables", "compid", "uninit")
            config.set("Environment Variables", "keyringMode", str(False))
            config.set("Environment Variables", "sign by default", str(True))
            config.set("Environment Variables", "signing fp", "0")
            config.set("Envrionment Variables", "Drive Letter", "D:/")
            config.set("Environment Variables", "uid",
                       "uninit")  # as a portable function this should work in both Linux and Windows
            if platform.system() == "Linux":  # Some defaults could be better
                uname = os.uname()
                config.set("Environment Variables", "compid",
                           str(uname[1]))  # gets the nodeid and sets it as the computer's name.
            configFile = os.open("tapestry.cfg", os.O_CREAT | os.O_RDWR)
            os.close(configFile)
            with open("tapestry.cfg", "r+") as t:
                config.write(t)

        ns.expectedFP = config.get("Environment Variables", "Expected FP")
        ns.fp = config.get("Environment Variables", "Expected FP")  # Can be changed during the finding process.
        ns.keyringMode = config.getboolean("Environment Variables", "keyringMode")
        ns.signing = config.getboolean("Environment Variables", "Sign by Default")
        ns.sigFP = config.get("Environment Variables", "Signing FP")

        # We also declare some globals here. They aren't used in the children so they aren't part of ns, but they still need to be declared and still come from config.
        global blockSizeActual;
        blockSizeActual = config.getint("Environment Variables", "blockSize") * (
        2 ** 20)  # cfg asks the user for MB, but for actual processes we need bytes
        global compid, compid = config.get("Environment Variables", "compid")
        global driveletter;
        driveletter = config.get("Environment Variables",
                                 "driveletter")  # The windows drive letter of the removable disk mount point. Used for rcv mode.
        global uid;
        uid = config.get("Environment Variables", "uid")  # Not sure actually used anywhere!


# Runtime
if __name__ == "__main__":
    announce()
    buildMaster()
    parseArgs()
    parseConfig()
    startLogger()
    if ns.uninit:
        init()
        checkGPGConfig()
        exit()
    elif ns.setup:
        setup()
        exit()
    elif ns.rcv:
        print("Tapestry is ready to recover your files. Please insert the first disk.")
        findKeyFile("sec")
        loadKey()
        print("Tapestry is using this secret key: %s" % ns.activeFP)
        print("Please enter the secret for this key. If none, leave blank.")
        secret = input(">")
        createDIRS()
        findblock()
        validateBlock()
        decryptBlock()
        openPickle()
        print("This backup exists in %d blocks." % numBlocks)
        for i in range(numBlocks - 1):
            input("Please insert the next disk and press enter to continue.")
            findBlock()
            validateBlock()
            decryptBlock()
        unpackBlocks()
        print("Any files with uncertain placement were moved to the desktop.")
        print("All blocks have now been unpacked. Tapestery will clean up and exit.")
        cleardown()
        exit()
    else:
        createDIRS()
        buildOpsList()  # TODO Define
        print("Tapestry is configuring itself. Please wait.")
        findKeyFile("pub")
        loadKey()
        print("Confirm this session will use the following key:")
        print(str(ns.activeFP))
        print("The expected FP is:")
        print(str(ns.activeFP))
        qcontinue = input("Continue? y/n>")
        if qucontinue.lower() != "y":
            cleardown()
            exit()
        print("Tapestry is preparing the backup index. This may take a few moments.")
        for category in ns.listRun:
            getContents(category, listRun[category])
        makeIndex()
        buildBlocks()
        enqueueBlockbuild()
        processBlockbuild()
        enqueueEncryption()
        processEncryption()
        if ns.signing:
            fetchSigningKey()
            enqueueSigning()
            processSigning()
        print("The processing has completed. Your .tap files are here:")
        print(str(ns.drop))
        print("Please archive these expediently.")
        cleardown()
        exit()