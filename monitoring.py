"""
This is the job module and supports all the REST actions for the
job data
"""

from flask import make_response, abort
from config import db
from models import Job, JobSchema


def read_all():
    """
    This function responds to a request for /api/job
    with the complete lists of job
    :return:        json string of list of job
    """
    # Create the list of job from our data
    job = Job.query.order_by(Job.job_id).all()

    # Serialize the data for the response
    job_schema = JobSchema(many=True)
    data = job_schema.dump(job)
    return data


def read_one(job_id):
    # Get the job requested
    job = Job.query.filter(Job.job_id == job_id).one_or_none()

    # Did we find a job?
    if job is not None:

        # Serialize the data for the response
        job_schema = JobSchema()
        data = job_schema.dump(job)
        return data

    # Otherwise, nope, didn't find that job
    else:
        abort(
            404,
            "Job not found for Id: {job_id}".format(job_id=job_id),
        )


def delete(job_id):
    # Get the job requested
    job = Job.query.filter(Job.job_id == job_id).one_or_none()

    # Did we find a job_id?
    if job is not None:
        db.session.delete(job)
        db.session.commit()
        return make_response(
            "Job {job_id} deleted".format(job_id=job_id), 200
        )

    # Otherwise, nope, didn't find that job
    else:
        abort(
            404,
            "Job not found for Id: {job_id}".format(job_id=job_id),
        )


def update(job_id, job):
    # Get the job requested from the db into session
    update_job = Job.query.filter(Job.job_id == job_id).one_or_none()

    # Try to find an existing job with the same name as the update
    job_id = job.get("job_id")
    app_name = job.get("app_name")
    state = job.get("state")

    existing_job = (
        Job.query.filter(Job.job_id == job_id)
        .filter(Job.app_name == app_name)
        .filter(Job.state == state)
        .one_or_none()
    )

    # Are we trying to find a job that does not exist?
    if update_job is None:
        abort(
            404,
            "Job not found for Id: {job_id}".format(job_id=job_id),
        )

    # Would our update create a duplicate of another job already existing?
    elif (
        existing_job is not None and existing_job.job_id != job_id
    ):
        abort(
            409,
            "Job {job_id} {app_name} exists already".format(
                job_id=job_id, app_name=app_name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in job into a db object
        schema = JobSchema()
        update = schema.load(job, session=db.session).data

        # Set the id to the job we want to update
        update.job_id = update_job.job_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated job in the response
        data = schema.dump(update_job)
        # data = schema.dump(update_job).data

        return data, 200


def create(job):

    job_id = job.get("job_id")
    app_name = job.get("app_name")
    state = job.get("state")

    existing_job = (
        Job.query.filter(Job.job_id == job_id)
        .filter(Job.app_name == app_name)
        .filter(Job.state == state)
        .one_or_none()
    )

    # Can we insert this job?
    if existing_job is None:

        # Create a job instance using the schema and the passed in job
        schema = JobSchema()
        # new_job = schema.load(job, session=db.session).data
        new_job = schema.load(job, session=db.session)

        # Add the job to the database
        db.session.add(new_job)
        db.session.commit()

        # Serialize and return the newly created job in the response
        data = schema.dump(new_job)

        return data, 201

    # Otherwise, nope, job exists already
    # else:
    #     abort(
    #         409,
    #         "Job {job_id} {app_name} {state} exists already".format(
    #             job_id=job_id, app_name=app_name, state=state
    #         ),
    #     )
