#!/bin/bash

celery -A src.tasks.celery_worker beat -l INFO