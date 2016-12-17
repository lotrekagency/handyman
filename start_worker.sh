#!/bin/bash

celery -A worker worker -l info -B
