# Azure AI Sessionize
In this project, you will find Python scripts that consume GPT-4 and Dalle3 through Azure AI services to automatically generate messages for X (Twitter) and very amusing images based on the information obtained from sessions and speakers of an event created with Sessionize.

## Introduction
Today I woke up early and remembered that I have to announce all the sessions that have been selected for the next event I have organized through Sessionize. So far, so good. But when I realized the amount of work I actually have to do, I felt a lot of laziness creeping in.
There are over 40 sessions, for each of which I'll have to create a compelling, unique message for X (Twitter), referencing the event's hashtag and the attendees' handles (which usually takes me quite a while to find).
And that's not all, because to do it properly, I'll have to design a coherent Twitter posting schedule, with spacing between each post, spread out over all the days leading up to the event date, etc.
But when I saw the possibility of exporting the data from Sessionize into CSV tables, an idea struck me: What if I ask GPT to do the work for me?
