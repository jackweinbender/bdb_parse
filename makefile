#! /bin/bash

default: parse-from-html
	
parse-from-html:
	@ cd parse-first-js && npm start	