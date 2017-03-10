from vboxapi import *

def createHddCmd(ctx, size,loc,fmt):

    hdd = ctx['vb'].createMedium(fmt, loc, ctx['global'].constants.AccessMode_ReadWrite, ctx['global'].constants.DeviceType_HardDisk)
    progress = hdd.createBaseStorage(size, (ctx['global'].constants.MediumVariant_Standard, ))
    if hdd.id:
        print("created HDD at %s as %s" % (hdd.location, hdd.id))
    else:
       print("cannot create disk (file %s exist?)" % (loc))
       return 0

    return 0

def listHdd(ctx):

    hdds = ctx['global'].getArray(ctx['vb'], 'hardDisks')
    print("Hard disks:")
    for hdd in hdds:
        if hdd.state != ctx['global'].constants.MediumState_Created:
            hdd.refreshState()
        print("   %s (%s)%s %s [logical %s]" % (hdd.location, hdd.format, hdd.id, hdd.size, hdd.logicalSize))



def hostCmd(ctx):
    vbox = ctx['vb']

    props = vbox.systemProperties
    print("Machines: %s" % (props.defaultMachineFolder))

    #print("Global shared folders:")
    #for ud in ctx['global'].getArray(vbox, 'sharedFolders'):
    #    printSf(ctx, sf)
    host = vbox.host
    cnt = host.processorCount
    print("Processors:")
    print("  available/online: %d/%d " % (cnt, host.processorOnlineCount))
    for i in range(0, cnt):
        print("  processor #%d speed: %dMHz %s" % (i, host.getProcessorSpeed(i), host.getProcessorDescription(i)))

    print("RAM:")
    print("  %dM (free %dM)" % (host.memorySize, host.memoryAvailable))
    print("OS:")
    print("  %s (%s)" % (host.operatingSystem, host.OSVersion))
    if host.acceleration3DAvailable:
        print("3D acceleration available")
    else:
        print("3D acceleration NOT available")

    print("Network interfaces:")
    for ni in ctx['global'].getArray(host, 'networkInterfaces'):
        print("  %s (%s)" % (ni.name, ni.IPAddress))

    return 0

def getMachines(ctx, invalidate = False, simple=False):
    if ctx['vb'] is not None:
        if ctx['_machlist'] is None or invalidate:
            ctx['_machlist'] = ctx['global'].getArray(ctx['vb'], 'machines')
            ctx['_machlistsimple'] = cacheMachines(ctx, ctx['_machlist'])
        if simple:
            return ctx['_machlistsimple']
        else:
            return ctx['_machlist']
    else:
        return []

def createVm(ctx, name, kind):

    try:
        ctx['vb'].getGuestOSType(kind)
    except Exception:
        print('Unknown OS type:', kind)
        return 0

    vbox = ctx['vb']
    #getMachines(ctx, True)
    mach = vbox.createMachine("", name, [], kind, "")
    mach.saveSettings()
    print("created machine with UUID", mach.id)
    vbox.registerMachine(mach)
    # update cache

#
# Converts an enumeration to a printable string.
#
def enumToString(constants, enum, elem):
    all = constants.all_values(enum)
    for e in all.keys():
        if str(elem) == str(all[e]):
            return e
    return "<unknown>"



if __name__ == "__main__":


    # This is a VirtualBox COM/XPCOM API client, no data needed.
    wrapper = VirtualBoxManager(None, None)

    # Get the VirtualBox manager
    mgr  = wrapper.mgr
    # Get the global VirtualBox object
    vbox = wrapper.vbox

    print("Running VirtualBox version %s" %(vbox.version))

    # Get all constants through the Python wrapper code
    vboxConstants = wrapper.constants

    vmList = []

    # Enumerate all defined machines
    for mach in wrapper.getArray(vbox, 'machines'):

        try:
            # Be prepared for failures - the VM can be inaccessible
            vmname = '<inaccessible>'
            try:
                vmname = mach.name
                vmList.append(vmname)
            except Exception as e:
                None
            vmid = '';
            try:
                vmid = mach.id
            except Exception as e:
                None

            # Print some basic VM information even if there were errors
            print("Machine name: %s [%s]" %(vmname, vmid))
            if vmname == '<inaccessible>' or vmid == '':
                continue

            # Print some basic VM information
            print("    State:           %s" %(enumToString(vboxConstants, "MachineState", mach.state)))
            print("    Session state:   %s" %(enumToString(vboxConstants, "SessionState", mach.sessionState)))

            # Do some stuff which requires a running VM
            if mach.state == vboxConstants.MachineState_Running:

                # Get the session object
                session = mgr.getSessionObject(vbox)

                 # Lock the current machine (shared mode, since we won't modify the machine)
                mach.lockMachine(session, vboxConstants.LockType_Shared)

                # Acquire the VM's console and guest object
                console = session.console
                guest = console.guest

                # Retrieve the current Guest Additions runlevel and print
                # the installed Guest Additions version
                addRunLevel = guest.additionsRunLevel
                print("    Additions State: %s" %(enumToString(vboxConstants, "AdditionsRunLevelType", addRunLevel)))
                if addRunLevel != vboxConstants.AdditionsRunLevelType_None:
                    print("    Additions Ver:   %s" % (guest.additionsVersion))

                # Get the VM's display object
                display = console.display

                # Get the VM's current display resolution + bit depth + position
                screenNum = 0 # From first screen
                (screenW, screenH, screenBPP, screenX, screenY, _) = display.getScreenResolution(screenNum)
                print("    Display (%d):     %dx%d, %d BPP at %d,%d" % (screenNum, screenW, screenH, screenBPP, screenX, screenY))

                # We're done -- don't forget to unlock the machine!
                session.unlockMachine()

        except Exception as e:
            print("Errror [%s]: %s" %(mach.name, str(e)))
            traceback.print_exc()


    ctx = {
        'global':       mgr,
        'vb':           mgr.vbox,
        'const':        mgr.constants,
        'remote':       mgr.remote,
        'type':         mgr.type
    }

    name = "TEST_VM"
    if name not in vmList:
        createVm(ctx,'TEST_VM','Ubuntu')


    #
    # obetnir les informations sur le host (pour log ??)
    #
    hostCmd(ctx)

    #
    # trouver une VM a partir du nom
    #
    mach = vbox.findMachine(name)

    #
    # session courante
    #
    session = mgr.mgr.getSessionObject(vbox)


    #
    # Creer un disque virtuel
    #
    _ret = createHddCmd(ctx, 1000, r'D:\VM_FWS\VM_A350\1_CentOS_6.3_64b_Simu_VMTools\CentOS_6.3_64b_Simu_VMTools','vdi')

    print(_ret)

    listHdd(ctx)
    #
    # lancement de la VM
    #
    progress = mach.launchVMProcess(session, "gui", "")

    #
    # boucle infini execution
    #
    progress.waitForCompletion(-1)


    # Call destructor and delete wrapper
    del wrapper