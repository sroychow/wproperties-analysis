#include "../interface/boostHweightsHelper.hpp"
/// This constructor takes all the parameters necessary to build the THnTs. In addition, it requires the names of
/// the columns which will be used.

int getIndex(std::vector<std::string> v, std::string K)
{
   auto it = std::find(v.begin(), v.end(), K);
   if (it != v.end())
   {
      int index = std::distance(v.begin(), it);
      return index;
   }
   else
   {
      //std::cout << "-1" << std::endl;
      return -1;
   }
}

boostHweightsHelper::boostHweightsHelper(std::string name,
                                         std::vector<std::string> weightNames,
                                         std::vector<float> bins1,
                                         std::vector<float> bins2,
                                         std::vector<float> bins3,
                                         std::vector<float> bins4,
                                         std::vector<float> bins5)
{
   _name = name;
   _weightNames = weightNames;
   _bins1 = bins1;
   _bins2 = bins2;
   _bins3 = bins3;
   _bins4 = bins4;
   _bins5 = bins5;

   _v.emplace_back(_bins1);
   _v.emplace_back(_bins2);
   _v.emplace_back(_bins3);
   _v.emplace_back(_bins4);
   _v.emplace_back(_bins5);

   const auto nSlots = ROOT::IsImplicitMTEnabled() ? ROOT::GetThreadPoolSize() : 1;

   for (auto slot : ROOT::TSeqU(nSlots))
   {
      fHistos.emplace_back(std::make_shared<std::map<std::string, boost_histogram>>());
      std::vector<std::string> sorted(_weightNames);
      for (auto &x : sorted)
         x = _name + x;
      fNames.emplace_back(std::make_shared<std::vector<std::string>>(sorted));
      (void)slot;

      std::map<std::string, boost_histogram> &hmap = *fHistos[slot];
      const auto n_histos = _weightNames.size();

      std::string slotnum = "";
      slotnum = slot > 0 ? std::to_string(slot) : "";
      for (unsigned int i = 0; i < n_histos; ++i)
      {
         auto htmp = boost::histogram::make_weighted_histogram(_v);
         hmap.insert(std::make_pair(std::string(_name + _weightNames[i]), htmp));
         //std::cout << hnames[i] << std::endl;
      }
   }
}

std::shared_ptr<std::map<std::string, boost_histogram>> boostHweightsHelper::GetResultPtr() const { return fHistos[0]; }
void boostHweightsHelper::Initialize() {}
void boostHweightsHelper::InitTask(TTreeReader *, unsigned int) {}
/// This is a method executed at every entry

void boostHweightsHelper::Exec(unsigned int slot, const ROOT::VecOps::RVec<float> &vars, const float &w, const ROOT::VecOps::RVec<float> &weights)
{
   std::map<std::string, boost_histogram> &hmap = *fHistos[slot];
   std::vector<std::string> &hnames = *fNames[slot];
   for (auto &x : hmap)
   {
      int i = getIndex(hnames, x.first);
      auto wtot = w * weights[i];
      double var1 = vars.size()>0 ? vars[0] : 0.;
      double var2 = vars.size()>1 ? vars[1] : 0.;
      double var3 = vars.size()>2 ? vars[2] : 0.;
      double var4 = vars.size()>3 ? vars[3] : 0.;
      double var5 = vars.size()>4 ? vars[4] : 0.;
      //std::cout << vars.size() << " "<< vars[0] << " " << var1 << " " << var2 << " " << var3 << " " << var4 << " " << var5 << std::endl;
      x.second(var1, var2, var3, var4, var5, boost::histogram::weight(wtot));
      //x.second(var1, var2, var3, var4, var5);
   }
}
/// This method is called at the end of the event loop. It is used to merge all the internal THnTs which
/// were used in each of the data processing slots.
void boostHweightsHelper::Finalize()
{
   auto &res = *fHistos[0];
   for (auto slot : ROOT::TSeqU(1, fHistos.size()))
   {
      auto &map = *fHistos[slot];
      for (auto &x : res)
      {
         x.second += map[x.first];
      }
   }
}
std::string boostHweightsHelper::GetActionName()
{
   return "boostHweightsHelper";
}
