/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef AXIONSUPERRADIANCELEVEL_HPP_
#define AXIONSUPERRADIANCELEVEL_HPP_

#include "BHAMR.hpp"
#include "DefaultLevelFactory.hpp"
#include "GRAMRLevel.hpp"
// Problem specific includes
#include "Potential.hpp"
#include "ScalarField.hpp"

//!  A class for the evolution of an axion (real scalar) field on a Kerr BH
/*!
     The class takes initial data for a scalar field (variables phi and Pi)
     laid down on a Kerr black hole background and evolves it using the CCZ4
     equations, to study axion superradiance. \sa MatterCCZ4(),
   ConstraintsMatter(), ScalarField()
*/
class AxionSuperradianceLevel : public GRAMRLevel
{
    friend class DefaultLevelFactory<AxionSuperradianceLevel>;
    // Inherit the contructors from GRAMRLevel
    using GRAMRLevel::GRAMRLevel;

    BHAMR &m_bh_amr = dynamic_cast<BHAMR &>(m_gr_amr);

    // Typedef for scalar field
    typedef ScalarField<Potential> ScalarFieldWithPotential;

    //! Things to do at the end of the advance step, after RK4 calculation
    virtual void specificAdvance() override;

    //! Initialize data for the field and metric variables
    virtual void initialData() override;

    //! Initialize data for the field and metric variables
    virtual void postRestart() override;

#ifdef CH_USE_HDF5
    //! routines to do before outputting plot file
    virtual void prePlotLevel() override;
#endif

    //! RHS routines used at each RK4 step
    virtual void specificEvalRHS(GRLevelData &a_soln, GRLevelData &a_rhs,
                                 const double a_time) override;

    //! Things to do in UpdateODE step, after soln + rhs update
    virtual void specificUpdateODE(GRLevelData &a_soln,
                                   const GRLevelData &a_rhs,
                                   Real a_dt) override;

    /// Things to do before tagging cells (i.e. filling ghosts)
    virtual void preTagCells() override;

    //! Tell Chombo how to tag cells for regridding
    virtual void computeTaggingCriterion(
        FArrayBox &tagging_criterion, const FArrayBox &current_state,
        const FArrayBox &current_state_diagnostics) override;

    //! to do post each time step on every level
    virtual void specificPostTimeStep() override;
};

#endif /* AXIONSUPERRADIANCELEVEL_HPP_ */
