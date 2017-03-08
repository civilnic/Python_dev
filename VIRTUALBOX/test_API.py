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
    mach = vbox.createMachine("", name, [], kind, "")
    mach.saveSettings()
    print("created machine with UUID", mach.id)
    vbox.registerMachine(mach)
    # update cache
    #getMachines(ctx, True)




if __name__ == "__main__":

    mgr = VirtualBoxManager(None, None)
    vbox = mgr.vbox

    ctx = {
        'global':       mgr,
        'vb':           mgr.vbox,
        'const':        mgr.constants,
        'remote':       mgr.remote,
        'type':         mgr.type
    }


    createVm(ctx,'TEST_VM','Ubuntu')



    #
    # lister les machines virtuelles
    #

    for m in mgr.getArray(vbox, 'machines'):
        print ("Machine ’%s’ logs in ’%s’" % (m.name, m.logFolder))

    name = "TEST_VM"


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