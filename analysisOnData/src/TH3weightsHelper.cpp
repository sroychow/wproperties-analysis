#include "interface/TH3weightsHelper.hpp"
   /// This constructor takes all the parameters necessary to build the THnTs. In addition, it requires the names of
   /// the columns which will be used.
   TH3weightsHelper::TH3weightsHelper(std::string name, std::string title, 
                    int nbinsX, std::vector<float> xbins,
                    int nbinsY, std::vector<float> ybins,
                    int nbinsZ, std::vector<float> zbins,
                    std::vector<std::string> weightNames
                    )
   {
      _name = name;
      _nbinsX = nbinsX;
      _xbins = xbins;
      _nbinsY = nbinsY;
      _ybins = ybins;
      _nbinsZ = nbinsZ;
      _zbins = zbins;
      _weightNames = weightNames;

      TH1::AddDirectory(false);

      const auto nSlots = ROOT::IsImplicitMTEnabled() ? ROOT::GetThreadPoolSize() : 1;
      for (auto slot : ROOT::TSeqU(nSlots)) {
         fHistos.emplace_back(std::make_shared<std::vector<TH3D*>>());
         (void)slot;

         std::vector<TH3D*>& histos = *fHistos[slot];
         auto n_histos = _weightNames.size();

         std::string slotnum = "";
         slotnum = slot > 0 ? std::to_string(slot) : "";

         for (unsigned int i = 0; i < n_histos; ++i){

            histos.emplace_back(new TH3D(std::string(_name + _weightNames[i] + slotnum).c_str(),
                                     std::string(_name + _weightNames[i] + slotnum).c_str(), _nbinsX, _xbins.data(), _nbinsY, _ybins.data(), _nbinsZ, _zbins.data()));

            histos.back()->SetDirectory(nullptr);
        }

      }
   }

   //This constructor functions in the same way as above but instead of weighting histos, it weights
  // var2 or y(=pT) with it's variations
   TH3weightsHelper::TH3weightsHelper(std::string name, std::string title, 
				      int nbinsX, std::vector<float> xbins,
				      int nbinsY, std::vector<float> ybins,
				      std::vector<std::string> varyNames,
				      int nbinsZ, std::vector<float> zbins
				      )
   {
      _name = name;
      _nbinsX = nbinsX;
      _xbins = xbins;
      _nbinsY = nbinsY;
      _ybins = ybins;
      _nbinsZ = nbinsZ;
      _zbins = zbins;
      _ptvarNames = varyNames;

      TH1::AddDirectory(false);

      const auto nSlots = ROOT::IsImplicitMTEnabled() ? ROOT::GetThreadPoolSize() : 1;
      for (auto slot : ROOT::TSeqU(nSlots)) {
         fHistos.emplace_back(std::make_shared<std::vector<TH3D*>>());
         (void)slot;

         std::vector<TH3D*>& histos = *fHistos[slot];
         auto n_histos = _ptvarNames.size();

         std::string slotnum = "";
         slotnum = slot > 0 ? std::to_string(slot) : "";

         for (unsigned int i = 0; i < n_histos; ++i){
            histos.emplace_back(new TH3D(std::string(_name + _ptvarNames[i] + slotnum).c_str(),
                                     std::string(_name + _ptvarNames[i] + slotnum).c_str(),
                                     _nbinsX, _xbins.data(),
                                     _nbinsY, _ybins.data(),
                                     _nbinsZ, _zbins.data()));

            histos.back()->SetDirectory(nullptr);
        }

      }
   }

   //needed in template builder;it weights                      
   // var2 or y(=pT) with it's variations X weightvec
   TH3weightsHelper::TH3weightsHelper(std::string name, std::string title, 
				      int nbinsX, std::vector<float> xbins,
				      int nbinsY, std::vector<float> ybins,
				      int nbinsZ, std::vector<float> zbins,
				      std::vector<std::string> varyNames,
				      std::vector<std::string> weightNames
				      )
   {
      _name = name;
      _nbinsX = nbinsX;
      _xbins = xbins;
      _nbinsY = nbinsY;
      _ybins = ybins;
      _nbinsZ = nbinsZ;
      _zbins = zbins;
      _ptvarNames = varyNames;
      _weightNames = weightNames;
      
      _hindices=new TH2I("hindices", ";pt;weight", _ptvarNames.size(), 0., _ptvarNames.size(), _weightNames.size(), 0, _weightNames.size());
      unsigned int ih=0;
      for (unsigned int ipt = 1; ipt < _ptvarNames.size()+1; ++ipt){
	for (unsigned int iw = 1; iw < _weightNames.size()+1; ++iw){
	  _hindices->SetBinContent(ipt, iw, ih);
	  ih++;
	}
      }

      TH1::AddDirectory(false);      
      
      const auto nSlots = ROOT::IsImplicitMTEnabled() ? ROOT::GetThreadPoolSize() : 1;
      for (auto slot : ROOT::TSeqU(nSlots)) {
         fHistos.emplace_back(std::make_shared<std::vector<TH3D*>>());
         (void)slot;

         std::vector<TH3D*>& histos = *fHistos[slot];
         //auto n_histos = _ptvarNames.size()*_weightNames.size();

         std::string slotnum = "";
         slotnum = slot > 0 ? std::to_string(slot) : "";

         for (unsigned int ipt = 0; ipt < _ptvarNames.size(); ++ipt){
	   for (unsigned int iw = 0; iw < _weightNames.size(); ++iw){
	     histos.emplace_back(new TH3D(std::string(_name + _weightNames[iw] + _ptvarNames[ipt] + slotnum).c_str(),
					  std::string(_name + _weightNames[iw] + _ptvarNames[ipt] + slotnum).c_str(),
					  _nbinsX, _xbins.data(),
					  _nbinsY, _ybins.data(),
					  _nbinsZ, _zbins.data()));
           
            histos.back()->SetDirectory(nullptr);
	   }
	 }

      }
   }

  
   std::shared_ptr<std::vector<TH3D*>> TH3weightsHelper::GetResultPtr() const { return fHistos[0]; }
   void TH3weightsHelper::Initialize() {}
   void TH3weightsHelper::InitTask(TTreeReader *, unsigned int) {}
   /// This is a method executed at every entry

   void TH3weightsHelper::Exec(unsigned int slot, const float &var1, const float &var2,  const float &var3, const float &weight, const  ROOT::VecOps::RVec<float> &weights)
{
    auto& histos = *fHistos[slot];
    const auto n_histos = histos.size();
    for (unsigned int i = 0; i < n_histos; ++i)
       histos[i]->Fill(var1, var2, var3, weight * weights[i]);
}

void TH3weightsHelper::Exec(unsigned int slot, const float &var1, const ROOT::VecOps::RVec<float> &var2vec, const float &var3, const float &weight)
{
    auto& histos = *fHistos[slot];
    const auto n_histos = histos.size();
    for (unsigned int i = 0; i < n_histos; ++i)
       histos[i]->Fill(var1, var2vec[i], var3, weight);
}

void TH3weightsHelper::Exec(unsigned int slot, const float &var1, const ROOT::VecOps::RVec<float> &var2vec, const float &var3, const float &weight,  const  ROOT::VecOps::RVec<float> &weights)
{
    auto& histos = *fHistos[slot];
    for (unsigned int ipt = 1; ipt < var2vec.size()+1; ++ipt){
      for (unsigned int iw = 1; iw < weights.size()+1; ++iw){
	unsigned int ih = int(_hindices->GetBinContent(_hindices->FindBin(ipt,iw)));
	histos[ih]->Fill(var1, var2vec[ipt], var3, weight*weights[iw]);
      }
    }
}



   /// This method is called at the end of the event loop. It is used to merge all the internal THnTs which
   /// were used in each of the data processing slots.
   void TH3weightsHelper::Finalize()
   {
      auto &res_vec = *fHistos[0];
      for (auto slot : ROOT::TSeqU(1, fHistos.size())) {
         auto& histo_vec = *fHistos[slot];
         for (auto i : ROOT::TSeqU(0, res_vec.size()))
           res_vec[i]->Add(histo_vec[i]);
      }
   }
   std::string TH3weightsHelper::GetActionName(){
      return "TH3weightsHelper";
   }
