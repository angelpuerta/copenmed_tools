# Copenmed 
Tool used to create the graph provided by the [CopenMed](http://copenmed.org/) organisation


## Getting setup

The libraries for this project can be found on **requirements.yaml**.
Install them via :
```
conda env create --file requirements.yml
```

## How to run
The project uses **flask**, to run it:
```
cd app
~\anaconda3\envs\copenmed_tools\Scripts\flask.exe run
```

The application by default starts on port 5000 (http://localhost:5000/). 

The client uses **angular** to run it:

```
cd cli
ng serve --open 
```

The client by default will launch on port 4200 (http://localhost:4200/)

