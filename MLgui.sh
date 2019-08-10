export MLGUI_PLUGIN_DIRS=/home/benoit/Documents/projets/Python/MLGui/plugins:
export LD_LIBRARY_PATH=/home/benoit/Documents/projets/C/MultiLayerPerceptron/install/debug/libbrain-1.0.0/lib:$LD_LIBRARY_PATH
export BRAIN_LOG_LEVEL="critical"

ML_RESOURCE_PATH=/home/benoit/Documents/projets/C/MultiLayerPerceptron/install/debug/libbrain-1.0.0/example

NETWORK_PATH=$ML_RESOURCE_PATH/test_train_network.xml
DATA_PATH=$ML_RESOURCE_PATH/test_train_data.xml
SETTING_PATH=$ML_RESOURCE_PATH/test_train_settings.xml

python MLgui.py -n $NETWORK_PATH -d $DATA_PATH -s $SETTING_PATH
