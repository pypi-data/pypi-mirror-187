/*################################################################################
  ##
  ##   Copyright (C) 2016-2020 Keith O'Hara
  ##
  ##   This file is part of the OptimLib C++ library.
  ##
  ##   Licensed under the Apache License, Version 2.0 (the "License");
  ##   you may not use this file except in compliance with the License.
  ##   You may obtain a copy of the License at
  ##
  ##       http://www.apache.org/licenses/LICENSE-2.0
  ##
  ##   Unless required by applicable law or agreed to in writing, software
  ##   distributed under the License is distributed on an "AS IS" BASIS,
  ##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  ##   See the License for the specific language governing permissions and
  ##   limitations under the License.
  ##
  ################################################################################*/

#ifndef OPTIM_MATOPS_POW

//

#ifdef OPTIM_ENABLE_ARMA_WRAPPERS
    #define OPTIM_MATOPS_POW(x,a) arma::pow(x,a)
#endif

#ifdef OPTIM_ENABLE_EIGEN_WRAPPERS
    #define OPTIM_MATOPS_POW(x,a) (x).array().pow(a).matrix()
#endif

//

#endif
