#ifndef BOOSTHWEIGHTSHELPER_H
#define BOOSTHWEIGHTSHELPER_H

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include <boost/histogram.hpp>
#include <memory>
#include <tuple>

//using boost_histogram = boost::histogram::histogram<std::tuple<boost::histogram::axis::variable<>, boost::histogram::axis::variable<>, boost::histogram::axis::variable<>, boost::histogram::axis::variable<>, boost::histogram::axis::variable<>>, boost::histogram::default_storage>;
using boost_histogram = boost::histogram::histogram<std::vector<boost::histogram::axis::variable<>>, boost::histogram::storage_adaptor<std::vector<boost::histogram::accumulators::weighted_sum<>, std::allocator<boost::histogram::accumulators::weighted_sum<>>>>>;

class boostHweightsHelper : public ROOT::Detail::RDF::RActionImpl<boostHweightsHelper>
{

public:
   /// This type is a requirement for every helper.
   using Result_t = std::map<std::string, boost_histogram>;

private:
   std::vector<std::shared_ptr<std::map<std::string, boost_histogram>>> fHistos; // one per data processing slot
   std::vector<std::shared_ptr<std::vector<std::string>>> fNames;                //to keep track of the ordering
   std::string _name;
   std::vector<std::string> _weightNames;
   std::vector<float> _bins1;
   std::vector<float> _bins2;
   std::vector<float> _bins3;
   std::vector<float> _bins4;
   std::vector<float> _bins5;
   std::vector<boost::histogram::axis::variable<>> _v;

public:
   /// This constructor takes all the parameters necessary to build the THnTs. In addition, it requires the names of
   /// the columns which will be used.
   boostHweightsHelper(std::string name,
                       std::vector<std::string> weightNames,
                       std::vector<float> bins1 = {0., 1.},
                       std::vector<float> bins2 = {0., 1.},
                       std::vector<float> bins3 = {0., 1.},
                       std::vector<float> bins4 = {0., 1.},
                       std::vector<float> bins5 = {0., 1.});

   boostHweightsHelper(boostHweightsHelper &&) = default;
   boostHweightsHelper(const boostHweightsHelper &) = delete;
   std::shared_ptr<std::map<std::string, boost_histogram>> GetResultPtr() const;
   void Initialize();
   void InitTask(TTreeReader *, unsigned int);
   /// This is a method executed at every entry

   void Exec(unsigned int slot, const ROOT::VecOps::RVec<float> &vars, const float &weight, const ROOT::VecOps::RVec<float> &weights);
   void Finalize();
   std::string GetActionName();
};

#endif
