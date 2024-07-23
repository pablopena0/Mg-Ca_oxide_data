Resultados de las simulaciones DFT para 55 óxidos de Mg y Ca, y algunas de sus deformaciones.

Explicación archivos:
	-> dft-results contiene los resultados de las 2703 deformaciones en formato XSF.
	
	-> ejemplo-MgO contiene un ejemplo de las simulaciones realizadas para el cristal de MgO. 
		qe-input se encarga de generar las deformaciones y enviar todos los archivos al gestor de colas slurm del cluster.
		Los outputs de Quantum ESPRESSO se encuentran dentro de la carpeta in-files.
	
	-> xsf-conver-script contiene los scripts de Python capaces de ordenar el output de Quantum ESPRESSO de los 55 cristales
	  en archivos los con formato XSF.
