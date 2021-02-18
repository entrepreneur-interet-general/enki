# Routes

## GET  /groups/types
> Return the list of group types (name and label)

Example
```
group_types: [
  {
    name: 'prefecture',
    label: 'Préfecture'
  }
  ...
]
```

## GET  /positions/{group_type_name} 
> return the list of existing positions in group types
  
Example: /positions/prefecture
```
positions: [
  {
    name: 'prefet',
    label: 'Préfet'
  }
  ...
]
```

## GET /locations/{group_type}
> return all possible location for this type

Example: /location/prefecture
```
locations: [
  {
    name: 'seine-et-marne',
    label: 'Seine-et-Marne'
  }
  ...
]
```

## POST /users
> create user and return the user newly created

Example:
```
body: {
  location: 'seine-et-marne', 
  first_name: 'Benjamin',
  last_name: 'PERNEY',
  position: 'prefet'
}

Return:
user: {
  location: 'seine-et-marne', 
  first_name: 'Benjamin',
  last_name: 'PERNEY',
  position: {
    name: 'prefet',
    label: 'Préfet',
    group: {
      name: 'prefecture',
      label: 'Préfecture'
    }
  }
}
```



