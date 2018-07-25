

def getNSigmaCrossSecMin(model, N=5, errorMax=0.001,lumi=300):
    outFile=open('/uscms_data/d3/eusai/danalysis/zp/plots/theta_'+lumi+'_'+str(N)+'sigmaSignif.txt','w')
    result={}
    
    signals=model.signal_process_groups.keys()
    #signals.sort(key=lambda x:int(x[re.search("\d",x).start():]))
    
    beta={}
    signif={}
    converged={}
    for signal in signals:
        if not beta.has_key(signal):
            beta[signal]=1
            signif[signal]=-999
            converged[signal]=False
            
    while True:
        
#        clean_workdir()
        signif=exp_significance_approx(model)

        for signal in signals:

            s=signif[signal]
            if abs(s-N)/s < errorMax:
                converged[signal]=True
                result[signal]=beta[signal]
                
            SF=N/s
            model.scale_predictions(SF,signal)  #for models with a single observable
            beta[signal]*=SF
            
            print signal, s

        allConverged=True
        for signal in signals:
            if not converged[signal]: allConverged=False
        if allConverged: break
        
    outFile.write("# Cross section for "+str(N)+" sigma significance:\n")
    for signal in signals:
        mass=''.join([str(s) for s in signal.split('_')[0] if s.isdigit()])
        outFile.write(mass+'   '+str(result[signal])+'\n')

    for signal in signals:
        model.scale_predictions(1/beta[signal],signal)


def get_model(lumi):
    # model = build_model_from_rootfile('/uscms_data/d3/eusai/danalysis/zp/plots/theta_'+lumi+'.root', include_mc_uncertainties = True)#mc uncertainties=true
    model = build_model_from_rootfile('/uscms_data/d3/eusai/danalysis/zp/plots/templates_RSGluon_pt500_forTHETA.root', include_mc_uncertainties = True)#mc uncertainties=true
    model.fill_histogram_zerobins()
    # model.set_signal_processes('rsg2*')
    model.set_signal_processes('Zprime*')
    #model.add_lognormal_uncertainty('ttbar_rate', math.log(1.15), 'ttbar')
    #model.add_lognormal_uncertainty('qcd_rate', math.log(1.15), 'qcd')
    for p in model.processes:
        #if p == 'qcd': continue
        model.add_lognormal_uncertainty('lumi', math.log(1.027), p)
        model.add_lognormal_uncertainty('trigger', math.log(1.03), p)
        #if 'signal' in p:
        #    model.add_lognormal_uncertainty(p+'_rate', math.log(1.15), p)
    return model

lumi='3000'
model = get_model(lumi)
model_summary(model)
# options = Options()
# options.set('main', 'n_threads', '20')
plot_exp,plot_obs = asymptotic_cls_limits(model,use_data=False)
#plot_exp, plot_obs = bayesian_limits(model,what='expected')#,n_toy = 2000, n_data = 20)
# plot_exp.write_txt('/uscms_data/d3/eusai/danalysis/zp/plots/theta_'+lumi+'.txt')
# report.write_html('/uscms_data/d3/eusai/danalysis/zp/plots/theta_'+lumi)
plot_exp.write_txt('/uscms_data/d3/eusai/danalysis/zp/plots/rsg.txt')
report.write_html('/uscms_data/d3/eusai/danalysis/zp/plots/rsg')

# getNSigmaCrossSecMin(model,5,0.001,lumi)
# getNSigmaCrossSecMin(model,3,0.001,lumi)