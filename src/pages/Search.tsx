import { useState } from "react";
import {
  Search as SearchIcon,
  User,
  KeyRound,
  Wallet,
  Globe,
  Shield,
  ArrowRight,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

const searchTypes = [
  {
    id: "actor",
    label: "Threat Actor",
    description: "Search by actor or persona name",
    icon: User,
  },
  {
    id: "handle",
    label: "Handle",
    description: "Search usernames and aliases",
    icon: SearchIcon,
  },
  {
    id: "pgp",
    label: "PGP Key",
    description: "Search cryptographic fingerprints",
    icon: KeyRound,
  },
  {
    id: "wallet",
    label: "Wallet",
    description: "Search cryptocurrency addresses",
    icon: Wallet,
  },
  {
    id: "domain",
    label: "Domain / Onion",
    description: "Search domains and onion services",
    icon: Globe,
  },
];

function Search() {
  const navigate = useNavigate();
  const [isSearching, setIsSearching] = useState(false);

  const handleActorSearch = () => {
    setIsSearching(true);

    setTimeout(() => {
      navigate("/actor-profile");
    }, 800);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <p className="text-sm font-medium uppercase tracking-wider text-blue-400">
          INVESTIGATION / SEARCH
        </p>

        <h1 className="mt-2 text-3xl font-semibold text-white">
          Threat Intelligence Search
        </h1>

        <p className="mt-2 max-w-2xl text-sm text-slate-400">
          Search across threat actors, handles, PGP keys, wallets and
          infrastructure indicators.
        </p>
      </div>

      {/* Search Box */}
      <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
        <div className="flex flex-col gap-3 md:flex-row">
          <div className="relative flex-1">
            <SearchIcon
              size={18}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
            />

            <input
              type="text"
              placeholder="Search actor, handle, wallet, PGP key or domain..."
              className="w-full rounded-lg border border-slate-800 bg-slate-950 py-3 pl-10 pr-4 text-sm text-white outline-none placeholder:text-slate-600 focus:border-blue-500/50"
            />
          </div>

          <button
            onClick={handleActorSearch}
            disabled={isSearching}
            className="flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-6 py-3 text-sm font-medium text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-70"
          >
            <SearchIcon size={16} />
            {isSearching ? "Searching..." : "Search"}
          </button>
        </div>
      </div>

      {/* Search Types */}
      <div>
        <div className="mb-5">
          <h2 className="text-lg font-semibold text-white">
            Search By Indicator
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Select an investigation data type to begin your search.
          </p>
        </div>

        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {searchTypes.map((type) => {
            const Icon = type.icon;

            return (
              <button
                key={type.id}
                onClick={type.id === "actor" ? handleActorSearch : undefined}
                className="group rounded-xl border border-slate-800 bg-slate-900 p-5 text-left transition hover:border-slate-700 hover:bg-slate-900/80"
              >
                <div className="flex items-start justify-between">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-500/10 text-blue-400">
                    <Icon size={19} />
                  </div>

                  <ArrowRight
                    size={17}
                    className="text-slate-700 transition group-hover:translate-x-1 group-hover:text-blue-400"
                  />
                </div>

                <h3 className="mt-5 text-sm font-semibold text-white">
                  {type.label}
                </h3>

                <p className="mt-2 text-xs leading-5 text-slate-500">
                  {type.description}
                </p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Investigation Notice */}
      <div className="rounded-xl border border-blue-500/20 bg-blue-500/5 p-5">
        <div className="flex items-start gap-4">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-blue-500/10 text-blue-400">
            <Shield size={19} />
          </div>

          <div>
            <h3 className="text-sm font-semibold text-white">
              Investigation Search
            </h3>

            <p className="mt-1 text-sm leading-6 text-slate-400">
              Search results can be used to investigate identities,
              relationships, infrastructure and AI-powered attribution
              findings.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Search;