## Project_Title

Automation Test Framework for WAKU project using python/docker 
the objective of the project is to write 2 test cases 
[test_basic_node_operation – test_Inter_Node_Communication ]



## Installation

1- clone the repo 
2- make sure the following installed 
   - python 3.10 or higher 
   packages in python 
    - docker in python version 5.0.3 or 7.1.0 use command pip3 install docker
    - logging
    -unittest
    - time
    - json
    -  sys
    - os 
    -subproccess 
    

## Usage

to run the main file of the test cases follow the following steps
1- open terminal in same location of main.py 
2- type python3 main.py 

test cases will run and you can check the logs in terminal 



## Details

 when running the above cmmaond test cases will run as following

![Screenshot from 2024-07-10 13-00-06](https://github.com/AYAHASSAN287/WAKU_Automation_Framework/assets/49167455/564d2513-e412-4a6f-8683-7d13c9f65d96)

    
![Untitled Diagram drawio (1)](https://github.com/AYAHASSAN287/WAKU_Automation_Framework/assets/49167455/b931ac86-4c49-4c33-926d-04fe1397490c)



## Project overview 


![Untitled Diagram drawio (1)](https://github.com/AYAHASSAN287/WAKU_Automation_Framework/assets/49167455/0df46e31-4688-4e6f-80ab-e28239b7b675)


as shown in the diagram the testcase class send requests to waku_handler class

waku handler manage all requests needed by the test class .

Rest handler manage all interactions of system calls like sending requests to get REST APIs data and send shell requests .

Docker handler manage all requests regarding docker in python .



## important_notes:

logging_custom class is used from stackoverflow question in the following link link .

Test case [ test_node_up ] is considered as smoke test or entry test to determine wether the main tests shal run or not but it’s not impelmented as it is not the scope of the task . 


-precondition test case isn’t impelemented but it shall include additional preconditions for entring the test cases 

-post condition test case is impelemnted to ensure that all open resources are closed after the test case .


-there are features not impelmented like automatic port assignation and getting the subnet & gateway as the scope is limited to the 2 test cases only 
