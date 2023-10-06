#!/bin/bash

celery -A src.tasks.celery_worker worker -l INFO -E