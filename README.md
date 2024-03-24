# Azure AI Sessionize
In this project, you will find Python scripts that consume GPT-4 and Dalle3 through Azure AI services to automatically generate messages for X (Twitter) and very amusing images based on the information obtained from sessions and speakers of an event created with Sessionize.

## Introduction
Today I woke up early and remembered that I have to announce all the sessions that have been selected for the next event I have organized through Sessionize. So far, so good. But when I realized the amount of work I actually have to do, I felt a lot of laziness creeping in.
There are over 40 sessions, for each of which I'll have to create a compelling, unique message for X (Twitter), referencing the event's hashtag and the attendees' handles (which usually takes me quite a while to find).

And that's not all, because to do it properly, I'll have to design a coherent Twitter posting schedule, with spacing between each post, spread out over all the days leading up to the event date, etc. But when I saw the possibility of exporting the data from Sessionize into CSV tables, an idea struck me: 
- What if I ask GPT to do the work for me?

# Quick Start

## Sign in to the Azure CLI
[Sign in](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli) to the Azure CLI or select Open Cloudshell.

## Create an Azure resource group
To create an Azure OpenAI resource, you need an Azure resource group. When you create a new resource through the Azure CLI, you can also create a new resource group or instruct Azure to use an existing group. The following example shows how to create a new resource group named OAIResourceGroup with the az group create command. The resource group is created in the East US location.

```shell
az group create \
--name OAIResourceGroup \
--location eastus
```

## Create a resource
Use the az cognitiveservices account create command to create an Azure OpenAI resource in the resource group. In the following example, you create a resource named MyOpenAIResource in the OAIResourceGroup resource group. When you try the example, update the code to use your desired values for the resource group and resource name, along with your Azure subscription ID <subscriptionID>.

```shell
az cognitiveservices account create \
--name MyOpenAIResource \
--resource-group OAIResourceGroup \
--location eastus \
--kind OpenAI \
--sku s0 \
--subscription <subscriptionID>
```

## Get the primary API key
To retrieve the access keys for the resource, use the az cognitiveservices account keys list command. In this example, we direct the command output through the jq JSON processor to locate the .key1 value.

When you try the example, update the code to use your values for the resource group and resource.

```shell
az cognitiveservices account keys list \
--name <myResourceName> \
--resource-group  <myResourceGroupName> \
| jq -r .key1
```

## Deploy GPT-4 model
To deploy a model, use the az cognitiveservices account deployment create command. In the following example, you deploy an instance of the gpt-4 model and give it the name gpt-4. When you try the example, update the code to use your values for the resource group and resource. You don't need to change the model-version, model-format or sku-capacity, and sku-name values.

```shell
az cognitiveservices account deployment create \
--name <myResourceName> \
--resource-group <myResourceGroupName> \
--deployment-name gpt-4 \
--model-name gpt-4 \
--model-version "1"  \
--model-format OpenAI \
--sku-capacity "1" \
--sku-name "Standard"
```



## Disclaimer
The content of this repository is a contribution intended to showcase the capabilities of large language models (LLMs) when used as pieces of code in software solutions. 
Instead of writing a complex application full of algorithms and many hours of programming, we will demonstrate that by using request engineering, we can achieve the same results or even better ones.
To make this possible, we will make elaborate requests that we will send to the GPT-4 and Dalle3 models without the need for any fine-tuning or RAG techniques.

This exercise allows us to explore the model's capabilities while Microsoft Azure's cloud provides us with the security of being able to work with our data in a private instance where our data is solely ours and isolated from other users.

This development is not a professional solution as it lacks many important details such as LLMOps, for which I recommend using [PromptFlow](https://github.com/microsoft/promptflow), for example.
Of course, you are free to use this code to create tweets for your Sessionize events, to play around, to learn, or for whatever purpose you wish. The only thing I ask in return is that you cite the original source when you do so and propose your changes if you deem it necessary.

All contributions are welcome!
