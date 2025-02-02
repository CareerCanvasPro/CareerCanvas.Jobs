provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr     = var.vpc_cidr
  cluster_name = var.cluster_name
}

module "eks" {
  source = "./modules/eks"
  
  cluster_name    = var.cluster_name
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.private_subnet_ids
  instance_types = ["t3.small"]
  desired_size   = 2
  min_size       = 1
  max_size       = 4
}

module "rds" {
  source = "./modules/rds"
  
  identifier     = "${var.environment}-careercanvas-db"
  instance_class = "db.t3.small"
  allocated_storage = 20
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.private_subnet_ids
}

module "elasticache" {
  source = "./modules/elasticache"
  
  cluster_id     = "${var.environment}-careercanvas-redis"
  node_type      = "cache.t3.micro"
  num_cache_nodes = 1
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.private_subnet_ids
}

module "ecs" {
  source = "./modules/ecs"
  
  environment  = var.environment
  service_name = var.service_name
  
  cpu_units    = 256
  memory_units = 512
  
  desired_count = 1
}

module "dynamodb" {
  source = "./modules/dynamodb"
  
  table_name = "${var.environment}-jobs"
  hash_key   = "job_url"
}