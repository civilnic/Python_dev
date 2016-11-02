from flot import flot
import sys

def main():

    print(sys.argv[1])

    flotFile = sys.argv[1]

    myFlot = flot(flotFile)

    # for _channel in myFlot.channel_ref.keys():
    #
    #     _channelObj=myFlot.channel_ref[_channel]
    #     _channelObj.pprint()

        # if _channelObj.hasDimChannel():
        #     _channelObj.pprint()
        #     print (_channelObj.name+": "+str(_channelObj.tabMin)+","+str(_channelObj.tabMax))


    for _model in myFlot.models_ref.keys():
        _modelObj = myFlot.models_ref[_model]
        _modelObj.pprint()
        for _portObj in _modelObj._ports_consum:
            _portObj.pprint()

main()