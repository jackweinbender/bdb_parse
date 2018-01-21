#! /bin/bash

default: parse-from-html
	
parse-from-html:
	@ cd first-pass-js && npm start	