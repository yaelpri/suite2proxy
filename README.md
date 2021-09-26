## Suite2Proxy

#### Remote suite2p computation scheduler (Web App)

| Contents                        |
|---------------------------------|
| Usage & Deployment instructions |
| Design                          |
| Web Flow                        |
| Data Structure                  |

##
##### Usage & Deployment instructions 

1. Run server on computer A
2. Browse to server's IP from computer B
3. Select mouse, date, experiment
4. Configure suite2p computation settings
5. Schedule suite2p computation
6. Wait for results to appear in system log


    Python 3.7+ is required


| command line                                                     | instructions                                                                                                      |
|------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| ``` python suite2proxy.py ```                                    | Display full help message                                                                                         |
| ``` python suite2proxy.py --data-root={PATH}  --ip=10.0.0.100``` | Start web-app (server-side) on host machine, serve on port 80 (default)<br><br>Data directory at {PATH}           |
| ``` python suite2proxy.py --data-root=suite2proxy\engine\test``` | Contains fake data. Use to test GUI                                                                               |
| ``` python main.py                                           ``` | Located in engine. Run the sanity method, for testing basic flow. "test" folder currently isn't contain real data |
| ``` chrome http://10.0.0.100/ ```                                | Open webpage in any browser (Only tested in Chromium)                                                             |  
  
###
#### Optional running arguments
* --data-root: path to directory containing mice names
* --ip: default ip "0.0.0.0"
* --port: default port "80"
* --data-extension: file type (default "sbx")
* --ops: optional argument. Option to add path to suite2p settings file (ops.npy)

###
##### Additional options
- Default settings and file format can be added in Engine

  
###
##### Design

                       suite2proxy             
                            └──────────┐
                                       ├─[ .log ]
                                    ┌──┴──┐
                [html]─┬─[img] ─── app   engine 
                [ js ]─┴─[css]   ┌──┘     └──┐
                               webpage      Worker
     ┌─────────┬─────────┬───────┴─────┬────────────┬─────────────┐
    Welcome   ViewLog   SelectMouse   SelectDate   ScheduleJob   ScheduleJobComplex

###
##### Web Flow

    / ................................................... Landing page
    ├───o /log .......................................... Realtime system log view 
    └─┬─o /mouse ........................................ Mouse selection  
      └─┬─o /date ....................................... Select all mouse-specific experiment's date 
        └─┬─o /schedule-job ............................. Suite2p param definitions, per mouse-specific experiment  
          ├──o /schedule-complex ──┐ .................... Link multiple experiments for a combined suite2p computation 
          │                        ├──> /register-job ... Register finalized job with computation server
          └────────────────────────┘              

###
##### Data Structure
 
Files and directories inside the <b> root data directory </b> must be ordered as follows:
    
    ROOT                        
     │                                
     ├─┬─ Mouse-1                     
     │ ├┬─ 2021-07-26                 
     │ │├── experiment-01             
     │ │└── experiment-02         
     │ └┬─ 2021-07-28              
     │  └── experiment-03         L0: Root Data directory at network storage
     ├─┬─ Mouse-2                 L1: One directory per individual Mouse              
     │ └┬─ 2021-08-01             L2: Multiple directories, one per date  
     │  └── experiment-04         L3: Multiple directories, one per experiment               
     ├─  . . .                    L4: 1 data file per experiment        
     └── Rat-N ─...             

###
*This code was written by Yael Prilutski*
