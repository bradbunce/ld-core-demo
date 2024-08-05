import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import React, { useState, useEffect, useContext } from "react";
import LoginContext from "@/utils/contexts/login";
import { useLDClient } from "launchdarkly-react-client-sdk";
import { generateSuggestedItemsFeatureExperimentResults } from "@/experimentation-automation/featureExperimentGeneratorFunctions";

export default function FeatureExperimentGenerator() {
  const client = useLDClient();
  const { updateAudienceContext } = useContext(LoginContext);
  const [expGenerator, setExpGenerator] = useState(false);
  const [progress, setProgress] = useState(0);

  const updateContext = async () => {
    updateAudienceContext();
  };

  useEffect(() => {
    if (expGenerator) {
      generateSuggestedItemsFeatureExperimentResults({
        client,
        updateContext,
        setProgress,
        setExpGenerator,
      });
    }
  }, [expGenerator]);


  return (
    <Dialog>
      <DialogTrigger asChild>
        <p className="font-bold font-sohnelight text-lg">Feature Results Generator (Marketplace)</p>
      </DialogTrigger>
      <DialogContent>
        {expGenerator ? (
          <div className="flex justify-center items-center h-52">
            <div className=" font-bold font-sohne justify-center items-center text-xl">
              Generating Data
              <br />
              <div className="flex items-center mt-2 justify-center">
                <p>{progress.toFixed(0)}% Complete</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex justify-center text-xl font-bold items-center h-full">
            <button
              onClick={() => setExpGenerator(true)}
              className="mt-2 bg-gradient-experimentation p-2 rounded-sm hover:text-black hover:brightness-125 text-white"
            >
              Generate Feature Experiment Results (MarketPlace)
            </button>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
