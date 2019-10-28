export MLGUI_PLUGIN_DIRS=/home/benoit/Documents/projets/C/MLPlugins/install/debug/mlplugins-1.0.0/plugins:
export LD_LIBRARY_PATH=/home/benoit/Documents/projets/C/MLPlugins/install/debug/mlplugins-1.0.0/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/home/benoit/Documents/projets/C/MLPlugins/install/debug/mlplugins-1.0.0:/home/benoit/Documents/projets/Python/MLGui:$PYTHONPATH
export BRAIN_LOG_LEVEL="critical"
export LC_NUMERIC=C

python MLgui.py
