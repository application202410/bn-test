
## Installation and Running the Project
This project comes with a Dockerfile to build and run it. I've also provided a Docker compose file for no better reason than it simplifies the build and run process to a single command.

```
docker compose up
```
That should build the image and run it for you in one go. 

I've also included a devcontainer.json file, which is more useful if you want to poke around at the code. This should be as simple as:
- Start up the devcontainer (e.g. in VSCode)
- It should install all dependencies
- You can then run the code from the command line in the src directory.

```
cd src
python main.py
```


## Approach
The brief (and my conversation) stressed the need to keep this simple, so I'm going to start by getting all the basics done, build and the recommendation algorithm and then see how much time I have left to play with it and improve it.

I've divided this into a few key tasks:
- Project setup and basic 'Hello World' run instructions
- General project structure
- Download and parse phase
- Person-Job matching phase
- Output


### Project setup
I've reviewed enough developer tests to know how much I appreciate decent, clear and fuss-free instructions to get the code running. For nice, universal ease the approach I'm going with is:
- devcontainer file for development
- simple Dockerfile for 'production' run
- Docker compose file just to save on running Docker commands: I want this to be a one-command launch.

This feels like a good balance between simplicity of use and setup.

### General project structure
Whilst there's an appeal to showing off here and splitting the project into multiple pieces - e.g. a Recommendation API that ingests data and responds to POST requests for individual people, I think that's probably outside the scope of this task.

Keeping a clear focus on the end goal, I'm going to have:
- A main executable script
- A downloader that does all the outwards requests and parses data
- An interchangeable recommendations engine
    - This will take all the parsed data and returns a map of Person->Jobs.
    - Interchangeable so I can play around with different versions as drop-in replacements.
- A formatter that takes the mapped recommendations and writes output
    - This could e.g. write to a DB, serialise to JSON, etc.
    - But here it will simply print to console.
- Tests
    - I'm not going to work towards 100% coverage, given time constraints but will write tests mainly to help me as I write new code.

### Download and parse phase
I've kept this very simple and not really added much error handling or validation. Even with the presumption that this is a trusted, internal API, there really ought to be _some_ handling of errors. I've not spent any time doing that here - these will simply fall over if the input data is broken.

### Matching Phase
This is obviously the heart of the problem. I've created a structure that allows for swapping in new engines to try new versions.

Approaches:
#### Dummy Matcher
This is just an available jobs search really. It gives everyone every job.

#### KeyWord Matcher
I massively underestimated how long this would take to do, which prevented me from getting on to the fun part (see next matcher).

It takes a step-by-step approach:
- Extract employment type from job (currently just "is it an internship")
- Extract high-level category from job (using manual keyword mapping)
- Now loop through members, trying each job for them:
    - If they specify internship, only give them internships
    - If they specify a category, only give them matching category jobs
    - If they specify location(s), only give them jobs that match a specified location

#### NLP Matcher
I'd very much hoped to get on to using `nltk` to extract Noun Phrases from the text, using the Morphology settings to work on concepts like negation.

Unfortunately I didn't really have the time to get there.

### Output
As per the brief, this is very simple. I've split it out as a 'formatter' so that it could be easily replaced by something more sophisticated but not done anything more clever than that. this implementation simply loops through the members and prints out an alphabetical list of jobs for them. 

I've separated out DEBUG and INFO logging. INFO is the requested output (names and recommendations) whilst DEBUG should show why each job was not matched to a member.

 ## Discussion
This was a fun project. The JSON data provided is almost deceptively simple but there's quite a lot to unpack in the text. I had very much hoped to spend some of the time playing with NLP approaches to pulling meaning from the text but have opted instead to do something much more manual with keyword matching.

There are some obvious limitations to my approach:
- It's not very flexible. To make pretty much any change to keywords we'll need to add them manually, which is potentially a labour-intensive job that will keep generating work.
- Locations are not handled very cleverly. I've used the Location field in the jobs JSON as my dictionary of locations rather than specifying any anywhere. This has some benefits (if a job in Bristol is added, Bristol becomes a location we scan for) but has no relative or hierarchical context to it at all - e.g. we don't know that Leeds is in Yorkshire, so can't offer nearby or same-county jobs.

Example output looks like this:
```
2024-10-19 14:47:01 | INFO | Job recommendations are as follows:
2024-10-19 14:47:01 | INFO | NAME: Joe (I'm a designer from London, UK)
2024-10-19 14:47:01 | INFO | RECOMMENDED JOBS:
2024-10-19 14:47:01 | INFO | - UX Designer (London)
2024-10-19 14:47:01 | INFO | NAME: Marta (I'm looking for an internship in London)
2024-10-19 14:47:01 | INFO | RECOMMENDED JOBS:
2024-10-19 14:47:01 | INFO | - Legal Internship (London)
2024-10-19 14:47:01 | INFO | - Sales Internship (London)
2024-10-19 14:47:01 | INFO | NAME: Hassan (I'm looking for a design job)
2024-10-19 14:47:01 | INFO | RECOMMENDED JOBS:
2024-10-19 14:47:01 | INFO | - UX Designer (London)
2024-10-19 14:47:01 | INFO | NAME: Grace (I'm looking for a job in marketing outside of London)
2024-10-19 14:47:01 | INFO | RECOMMENDED JOBS:
2024-10-19 14:47:01 | INFO | <None>
2024-10-19 14:47:01 | INFO | NAME: Daisy (I'm a software developer currently in Edinburgh but looking to relocate to London)
2024-10-19 14:47:01 | INFO | RECOMMENDED JOBS:
2024-10-19 14:47:01 | INFO | - Data Scientist (London)
2024-10-19 14:47:01 | INFO | - Software Developer (London)
2024-10-19 14:47:01 | INFO | - Software Developer (Edinburgh)
```

- Joe: this seems the correct recommendation
- Marta: this seems the correct recommendation
- Hasan: this seems the correct recommendation
- Grace: I considered this a failure at first but have changed my mind. Negative searching is hard and often doesn't work well. Realistically, Grace is going to get better results if they specify where they _do_ want to work rather than where they don't.
- Daisy: they probably didn't want the Edinburgh recommendation. Or... did they? Someone who is only looking for jobs in London probably doesn't specify where they currently are. Perhaps a really good job where Daisy is currently based would convince them to stay?
