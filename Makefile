lint:  ## validate every seed against schema
	@find seed_vault -name "*.json" -exec python scripts/seed-linter.py {} \;

sim:   ## quick ethics sim
	@python scripts/ethics-simulator.py --action "$(ACTION)" --agent AI --affected human

up:    ## full stack
	docker-compose up --build

down:
	docker-compose down -v