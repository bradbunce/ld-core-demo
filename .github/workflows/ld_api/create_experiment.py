import os
import requests
import json
import shutil
from ruamel.yaml import YAML
import yaml
import base64
import time
 

def main():
    
    createFunnelExperiment()
    createFeatureExperiment()
    createAIFeatureExperiment()

def createAIFeatureExperiment():
    
    ld_api_key = os.getenv('LD_API_KEY')
    namespace = os.getenv('NAMESPACE')
    project_key = f"{namespace}-ld-demo"

    if not ld_api_key:
        print("LD_API_KEY not set")
        exit(1)
        
    if not namespace:
        print("NAMESPACE not set")
        exit(1)
        
    variations = getAIFeatureFlagDetails()
            
    url = "https://app.launchdarkly.com/api/v2/projects/" + project_key + "/environments/" + namespace + "/experiments"
    
    payload = {
        "name": "AI Chatbot Experiment",
        "description": "Track which models are providing the best user experience",
        "maintainerId": "6127d90d9971632664df6f1a",
        "key": "ai-chatbot-experiment",
        "iteration": {
            "hypothesis": "Which AI Models are providing best experiences to customers and delivering best responses",
            "canReshuffleTraffic": True,
            "metrics": [
            {
                "key": "ai-chatbot-good-service",
                "isGroup": False,
            },
            {
                "key": "ai-chatbot-bad-service",
                "isGroup": False,
            }
            ],
            "primarySingleMetricKey": "ai-chatbot-good-service",
            "treatments": [
                {
                    "name": variations[0]['name'],
                    "baseline": True,
                    "allocationPercent": "33",
                    "parameters": [
                    {
                        "flagKey": "ai-chatbot",
                        "variationId": variations[0]['_id']
                    }
                    ]
                },
                {
                    "name": variations[1]['name'],
                    "allocationPercent": "33",
                    "parameters": [
                    {
                        "flagKey": "ai-chatbot",
                        "variationId": variations[1]['_id']
                    }
                    ]
                },
                {
                    "name": variations[2]['name'],
                    "allocationPercent": "33",
                    "parameters": [
                    {
                        "flagKey": "ai-chatbot",
                        "variationId": variations[2]['_id']
                    }
                    ]
                },
            ],
            "flags": {
            "ai-chatbot": {
                "ruleId": "fallthrough",
                "flagConfigVersion": 1
            },
            },
            "randomizationUnit": "audience"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": ld_api_key,
        "LD-API-Version": "beta"
    }
    
    response = requests.post(url, json=payload, headers=headers)

    while True:
        if response.status_code == 201:
            print("Feature Experiment created successfully")
            break
        elif response.status_code == 429:
            print("Rate limit exceeded, waiting 10 seconds to retry...")
            time.sleep(10)
        else:
            data = response.json()
            print(data)
            print(response.status_code)
            break
    
def getAIFeatureFlagDetails():
    ld_api_key = os.getenv('LD_API_KEY')
    namespace = os.getenv('NAMESPACE')
    project_key = f"{namespace}-ld-demo"
    flag_key = "ai-chatbot"
    
    if not ld_api_key:
        print("LD_API_KEY not set")
        exit(1)
    
    if not namespace:
        print("NAMESPACE not set")
        exit(1)
        
    url = "https://app.launchdarkly.com/api/v2/flags/" + project_key + "/" + flag_key
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": ld_api_key,
    }
    while True:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("Flag details retrieved successfully")
            return response.json().get("variations")
        elif response.status_code == 429:
            print("Rate limit exceeded, waiting 10 seconds to retry...")
            time.sleep(5)
        else:
            print("Failed to retrieve flag details")
            exit(1)
              
def getFeatureFlagDetails():
    
    ld_api_key = os.getenv('LD_API_KEY')
    namespace = os.getenv('NAMESPACE')
    project_key = f"{namespace}-ld-demo"
    flag_key = "cartSuggestedItems"
    
    if not ld_api_key:
        print("LD_API_KEY not set")
        exit(1)
    
    if not namespace:
        print("NAMESPACE not set")
        exit(1)
        
    url = "https://app.launchdarkly.com/api/v2/flags/" + project_key + "/" + flag_key
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": ld_api_key,
    }
    while True:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("Flag details retrieved successfully")
            return response.json().get("variations")
        elif response.status_code == 429:
            print("Rate limit exceeded, waiting 10 seconds to retry...")
            time.sleep(5)
        else:
            print("Failed to retrieve flag details")
            exit(1)

def createFeatureExperiment():
    
    ld_api_key = os.getenv('LD_API_KEY')
    namespace = os.getenv('NAMESPACE')
    project_key = f"{namespace}-ld-demo"

    if not ld_api_key:
        print("LD_API_KEY not set")
        exit(1)
        
    if not namespace:
        print("NAMESPACE not set")
        exit(1)
        
    variations = getFeatureFlagDetails()
        
    url = "https://app.launchdarkly.com/api/v2/projects/" + project_key + "/environments/" + namespace + "/experiments"
    
    payload = {
        "name": "Upsell Tracking Experiment",
        "description": "Track if the new cart suggested component is driving greater upsell conversion",
        "maintainerId": "6127d90d9971632664df6f1a",
        "key": "upsell-tracking-experiment",
        "iteration": {
            "hypothesis": "If we enable the new cart suggested items feature, we can drive greater upsell conversion.",
            "canReshuffleTraffic": True,
            "metrics": [
            {
                "key": "upsell-tracking",
                "isGroup": False,
            },
            {
                "key": "in-cart-total-price",
                "isGroup": False,
            }
            ],
            "primarySingleMetricKey": "upsell-tracking",
            "treatments": [
                {
                    "name": variations[0]['name'],
                    "baseline": True,
                    "allocationPercent": "50",
                    "parameters": [
                    {
                        "flagKey": "cartSuggestedItems",
                        "variationId": variations[0]['_id']
                    }
                    ]
                },
                {
                    "name": variations[1]['name'],
                    "allocationPercent": "50",
                    "parameters": [
                    {
                        "flagKey": "cartSuggestedItems",
                        "variationId": variations[1]['_id']
                    }
                    ]
                },
            ],
            "flags": {
            "cartSuggestedItems": {
                "ruleId": "fallthrough",
                "flagConfigVersion": 1
            },
            },
            "randomizationUnit": "audience"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": ld_api_key,
        "LD-API-Version": "beta"
    }
    
    response = requests.post(url, json=payload, headers=headers)

    while True:
        if response.status_code == 201:
            print("Cart Suggested Items Feature Experiment created successfully")
            break
        elif response.status_code == 429:
            print("Rate limit exceeded, waiting 10 seconds to retry...")
            time.sleep(10)
        else:
            data = response.json()
            print(data)
            print(response.status_code)
            break

def getFunnelFeatureFlagDetails():
        
        ld_api_key = os.getenv('LD_API_KEY')
        namespace = os.getenv('NAMESPACE')
        project_key = f"{namespace}-ld-demo"
        flag_key = "storeAttentionCallout"
        
        if not ld_api_key:
            print("LD_API_KEY not set")
            exit(1)
        
        if not namespace:
            print("NAMESPACE not set")
            exit(1)
            
        url = "https://app.launchdarkly.com/api/v2/flags/" + project_key + "/" + flag_key
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": ld_api_key,
        }
        while True:
            response = requests.get(url, headers=headers)

            
            if response.status_code == 200:
                print("Flag details retrieved successfully")
                return response.json().get("variations")
            elif response.status_code == 429:
                print("Rate limit exceeded, waiting 10 seconds to retry...")
                time.sleep(5)
            else:
                print("Failed to retrieve flag details")
                exit(1)
            
            
def createFunnelExperiment():
    
    ld_api_key = os.getenv('LD_API_KEY')
    namespace = os.getenv('NAMESPACE')
    project_key = f"{namespace}-ld-demo"

    if not ld_api_key:
        print("LD_API_KEY not set")
        exit(1)
        
    if not namespace:
        print("NAMESPACE not set")
        exit(1)
        
    variations = getFunnelFeatureFlagDetails()
        
    url = "https://app.launchdarkly.com/api/v2/projects/" + project_key + "/environments/" + namespace + "/experiments"
    
    payload = {
        "name": "Grow engagement with key stores",
        "description": "If we adjust the header text to better copy we can drive greater attention into the stores in question, and greater conversion of checkout activities.",
        "maintainerId": "6127d90d9971632664df6f1a",
        "key": "grow-engagement-funnel-experiment",
        "iteration": {
            "hypothesis": "If we adjust the header text to better copy we can drive greater attention into the stores in question, and greater conversion of checkout activities.",
            "canReshuffleTraffic": True,
            "metrics": [
            {
                "key": "store-checkout-metrics",
                "isGroup": True,
            },
            {
                "key": "in-cart-total-price",
                "isGroup": False,
            }
            ],
            "primaryFunnelKey": "store-checkout-metrics",
            "treatments": [
                {
                    "name": variations[0]['name'],
                    "baseline": True,
                    "allocationPercent": "33",
                    "parameters": [
                    {
                        "flagKey": "storeAttentionCallout",
                        "variationId": variations[0]['_id']
                    }
                    ]
                },
                {
                    "name": variations[1]['name'],
                    "allocationPercent": "33",
                    "parameters": [
                    {
                        "flagKey": "storeAttentionCallout",
                        "variationId": variations[1]['_id']
                    }
                    ]
                },
                {
                    "name": variations[2]['name'],
                    "allocationPercent": "33",
                    "parameters": [
                    {
                        "flagKey": "storeAttentionCallout",
                        "variationId": variations[2]['_id']
                    }
                    ]
                
                }
            ],
            "flags": {
            "storeAttentionCallout": {
                "ruleId": "fallthrough",
                "flagConfigVersion": 1
            },
            },
            "randomizationUnit": "audience"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": ld_api_key,
        "LD-API-Version": "beta"
    }
    
    response = requests.post(url, json=payload, headers=headers)

    while True:
        if response.status_code == 201:
            print("Store Headers Funnel Experiment created successfully")
            break
        elif response.status_code == 429:
            print("Rate limit exceeded, waiting 10 seconds to retry...")
            time.sleep(10)
        else:
            data = response.json()
            print(data)
            print(response.status_code)
            break
        
if __name__ == "__main__":
    main()